#!/usr/bin/env python3
"""
Experiment 3: Semantic Autoencoder

Hypothesis: An autoencoder trained on color vocabulary will have high
reconstruction loss for non-color terms.

Method:
1. Build training set from known color names (Centore + curated)
2. Train character-level seq2seq autoencoder
3. Measure reconstruction loss on XKCD names
4. High loss = likely not a valid color name

Variants:
- Character-level: encode/decode character sequences
- With SBERT: use SBERT embeddings as input features
"""

import json
import time
import argparse
from pathlib import Path
from collections import Counter
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from common import (
    load_xkcd_names, load_centore_names, get_test_set,
    BASIC_COLORS, COLOR_MODIFIERS, preprocess_name, save_results,
    INVESTIGATION_DIR
)


# Character vocabulary
CHARS = " abcdefghijklmnopqrstuvwxyz'-"
CHAR_TO_IDX = {c: i for i, c in enumerate(CHARS)}
IDX_TO_CHAR = {i: c for c, i in CHAR_TO_IDX.items()}
PAD_IDX = len(CHARS)
MAX_LEN = 50


def encode_name(name: str) -> list:
    """Encode name as list of character indices."""
    name = name.lower()[:MAX_LEN]
    return [CHAR_TO_IDX.get(c, PAD_IDX) for c in name]


def decode_indices(indices: list) -> str:
    """Decode indices back to string."""
    return ''.join(IDX_TO_CHAR.get(i, '?') for i in indices if i != PAD_IDX)


class ColorNameDataset(Dataset):
    """Dataset of color names for autoencoder training."""

    def __init__(self, names: list, max_len: int = MAX_LEN):
        self.names = [preprocess_name(n) for n in names]
        self.max_len = max_len

    def __len__(self):
        return len(self.names)

    def __getitem__(self, idx):
        name = self.names[idx]
        encoded = encode_name(name)

        # Pad to max length
        padded = encoded + [PAD_IDX] * (self.max_len - len(encoded))
        return torch.tensor(padded[:self.max_len], dtype=torch.long)


class CharAutoencoder(nn.Module):
    """Character-level autoencoder for color names."""

    def __init__(self, vocab_size: int, embed_dim: int = 32,
                 hidden_dim: int = 64, latent_dim: int = 32):
        super().__init__()

        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.hidden_dim = hidden_dim
        self.latent_dim = latent_dim

        # Encoder
        self.embedding = nn.Embedding(vocab_size + 1, embed_dim, padding_idx=PAD_IDX)
        self.encoder_lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True,
                                     bidirectional=True)
        self.encoder_fc = nn.Linear(hidden_dim * 2, latent_dim)

        # Decoder
        self.decoder_fc = nn.Linear(latent_dim, hidden_dim)
        self.decoder_lstm = nn.LSTM(embed_dim + hidden_dim, hidden_dim,
                                     batch_first=True)
        self.output_fc = nn.Linear(hidden_dim, vocab_size + 1)

    def encode(self, x):
        """Encode input to latent representation."""
        # x: (batch, seq_len)
        embedded = self.embedding(x)  # (batch, seq_len, embed_dim)
        _, (h, _) = self.encoder_lstm(embedded)
        # Concatenate forward and backward hidden states
        h = torch.cat([h[0], h[1]], dim=-1)  # (batch, hidden_dim * 2)
        latent = self.encoder_fc(h)  # (batch, latent_dim)
        return latent

    def decode(self, latent, seq_len: int):
        """Decode latent to output sequence."""
        batch_size = latent.size(0)

        # Initial hidden state from latent
        h = self.decoder_fc(latent).unsqueeze(0)  # (1, batch, hidden_dim)
        c = torch.zeros_like(h)

        # Start with zeros
        decoder_input = torch.zeros(batch_size, 1, self.embed_dim,
                                     device=latent.device)

        outputs = []
        for _ in range(seq_len):
            # Concatenate latent to decoder input
            latent_expanded = latent.unsqueeze(1)  # (batch, 1, latent_dim)
            combined = torch.cat([decoder_input,
                                   self.decoder_fc(latent_expanded)], dim=-1)

            output, (h, c) = self.decoder_lstm(combined, (h, c))
            logits = self.output_fc(output)  # (batch, 1, vocab_size)
            outputs.append(logits)

            # Teacher forcing: use ground truth embedding
            decoder_input = torch.zeros(batch_size, 1, self.embed_dim,
                                          device=latent.device)

        return torch.cat(outputs, dim=1)  # (batch, seq_len, vocab_size)

    def forward(self, x):
        """Full forward pass."""
        latent = self.encode(x)
        output = self.decode(latent, x.size(1))
        return output, latent

    def reconstruction_loss(self, x):
        """Compute reconstruction loss for input."""
        output, _ = self.forward(x)
        # Flatten for cross entropy
        output_flat = output.view(-1, self.vocab_size + 1)
        target_flat = x.view(-1)
        loss = nn.functional.cross_entropy(output_flat, target_flat,
                                            ignore_index=PAD_IDX,
                                            reduction='none')
        # Average per sequence
        mask = (x != PAD_IDX).float()
        seq_lens = mask.sum(dim=1)
        loss = loss.view(x.size(0), -1)
        loss = (loss * mask).sum(dim=1) / seq_lens.clamp(min=1)
        return loss


def build_training_set() -> list:
    """Build training set from known color vocabulary."""
    names = set()

    # Centore names
    centore = load_centore_names()
    names.update(centore)

    # Basic colors and modifiers
    names.update(BASIC_COLORS)
    for modifier in ['light', 'dark', 'bright', 'pale', 'deep', 'vivid',
                      'soft', 'muted', 'dusty', 'pastel']:
        for color in BASIC_COLORS:
            names.add(f"{modifier} {color}")

    # Compound colors
    for c1 in ['blue', 'green', 'red', 'yellow', 'purple', 'orange', 'pink', 'brown']:
        for c2 in ['blue', 'green', 'red', 'yellow', 'purple', 'orange', 'pink', 'brown']:
            if c1 != c2:
                names.add(f"{c1}ish {c2}")
                names.add(f"{c1} {c2}")

    # Metaphorical colors
    metaphors = [
        'sky blue', 'grass green', 'lemon yellow', 'cherry red',
        'forest green', 'ocean blue', 'sunset orange', 'midnight blue',
        'rose pink', 'chocolate brown', 'cream white', 'coal black',
        'blood red', 'sea green', 'sand beige', 'moss green',
        'robin egg blue', 'olive green', 'burnt orange', 'wine red'
    ]
    names.update(metaphors)

    return list(names)


def train_autoencoder(model, train_loader, epochs: int = 50,
                       lr: float = 0.001, device: str = 'cpu'):
    """Train the autoencoder."""
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    losses = []
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for batch in train_loader:
            batch = batch.to(device)
            optimizer.zero_grad()

            loss = model.reconstruction_loss(batch).mean()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        avg_loss = epoch_loss / len(train_loader)
        losses.append(avg_loss)

        if (epoch + 1) % 10 == 0:
            print(f"   Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")

    return losses


def run_small_scale():
    """Run experiment on test set first."""
    print("=" * 70)
    print("Experiment 3: Semantic Autoencoder (Small Scale)")
    print("=" * 70)
    print()

    device = 'mps' if torch.backends.mps.is_available() else 'cpu'
    print(f"Using device: {device}")
    print()

    # Build training set
    print("1. Building training set...")
    train_names = build_training_set()
    print(f"   Training set size: {len(train_names)}")
    print(f"   Sample: {train_names[:5]}")
    print()

    # Create dataset and loader
    train_dataset = ColorNameDataset(train_names)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # Initialize model
    print("2. Initializing model...")
    vocab_size = len(CHARS)
    model = CharAutoencoder(vocab_size)
    print(f"   Parameters: {sum(p.numel() for p in model.parameters()):,}")
    print()

    # Train
    print("3. Training autoencoder...")
    losses = train_autoencoder(model, train_loader, epochs=50, device=device)
    print()

    # Evaluate on training set
    print("4. Evaluating on training set...")
    model.eval()
    with torch.no_grad():
        train_tensor = torch.stack([train_dataset[i] for i in range(len(train_dataset))])
        train_tensor = train_tensor.to(device)
        train_losses = model.reconstruction_loss(train_tensor).cpu().numpy()

    print(f"   Training loss: mean={np.mean(train_losses):.4f}, "
          f"std={np.std(train_losses):.4f}")
    print()

    # Test on curated test set
    print("5. Testing on curated test set...")
    test_set = get_test_set()
    results = {'training_losses': losses, 'test_results': {}}

    for category, names in test_set.items():
        if category.startswith('edge_'):
            continue

        if isinstance(names[0], tuple):
            test_names = [n[0] for n in names]
        else:
            test_names = names

        print(f"\n   Category: {category}")

        # Encode and compute loss
        test_dataset = ColorNameDataset(test_names)
        test_tensor = torch.stack([test_dataset[i] for i in range(len(test_dataset))])
        test_tensor = test_tensor.to(device)

        with torch.no_grad():
            test_losses = model.reconstruction_loss(test_tensor).cpu().numpy()

        results['test_results'][category] = {
            'names': test_names,
            'losses': test_losses.tolist(),
            'mean_loss': float(np.mean(test_losses)),
            'std_loss': float(np.std(test_losses))
        }

        print(f"   Mean loss: {np.mean(test_losses):.4f} "
              f"(std={np.std(test_losses):.4f})")

    # Threshold analysis
    print("\n6. Threshold analysis...")
    valid_losses = []
    invalid_losses = []

    for cat, data in results['test_results'].items():
        if 'valid' in cat:
            valid_losses.extend(data['losses'])
        elif 'invalid' in cat:
            invalid_losses.extend(data['losses'])

    valid_losses = np.array(valid_losses)
    invalid_losses = np.array(invalid_losses)

    print(f"   Valid colors: mean={np.mean(valid_losses):.4f}")
    print(f"   Invalid: mean={np.mean(invalid_losses):.4f}")

    # Find best threshold
    best_f1 = 0
    best_threshold = 0

    for threshold in np.arange(0.5, 3.0, 0.1):
        # Lower loss = more likely valid color
        tp = np.sum(valid_losses <= threshold)
        fp = np.sum(invalid_losses <= threshold)
        fn = np.sum(valid_losses > threshold)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    results['threshold_analysis'] = {
        'best_threshold': float(best_threshold),
        'best_f1': float(best_f1),
        'valid_mean': float(np.mean(valid_losses)),
        'invalid_mean': float(np.mean(invalid_losses))
    }

    print(f"   Best threshold: {best_threshold:.3f} (F1={best_f1:.3f})")

    # Save model and results
    torch.save(model.state_dict(), INVESTIGATION_DIR / 'exp3_autoencoder_model.pt')
    save_results(results, 'exp3_autoencoder_small_results.json')

    return results, model


def run_full_scale(model=None, batch_size: int = 1000):
    """Run on full XKCD dataset."""
    print()
    print("=" * 70)
    print("Experiment 3: Semantic Autoencoder (Full Scale)")
    print("=" * 70)
    print()

    device = 'mps' if torch.backends.mps.is_available() else 'cpu'

    if model is None:
        print("1. Loading trained model...")
        vocab_size = len(CHARS)
        model = CharAutoencoder(vocab_size)
        model.load_state_dict(torch.load(INVESTIGATION_DIR / 'exp3_autoencoder_model.pt'))
    else:
        print("1. Using provided model...")

    model = model.to(device)
    model.eval()
    print()

    # Load XKCD names
    print("2. Loading XKCD names...")
    xkcd_data = load_xkcd_names()
    names = list(xkcd_data.keys())
    counts = [xkcd_data[n] for n in names]
    print(f"   Loaded {len(names):,} names")
    print()

    # Process in batches
    print(f"3. Computing reconstruction losses (batch_size={batch_size})...")
    all_losses = []

    start_time = time.time()
    for i in range(0, len(names), batch_size):
        batch_names = names[i:i + batch_size]
        batch_dataset = ColorNameDataset(batch_names)
        batch_tensor = torch.stack([batch_dataset[j]
                                     for j in range(len(batch_dataset))])
        batch_tensor = batch_tensor.to(device)

        with torch.no_grad():
            losses = model.reconstruction_loss(batch_tensor).cpu().numpy()
        all_losses.extend(losses.tolist())

        if (i // batch_size) % 50 == 0 and i > 0:
            elapsed = time.time() - start_time
            progress = (i + len(batch_names)) / len(names)
            print(f"   Processed {i + len(batch_names):,}/{len(names):,} "
                  f"({progress * 100:.1f}%)")

    print(f"   Total time: {(time.time() - start_time):.1f} seconds")
    print()

    # Analyze results
    print("4. Analyzing results...")
    all_losses = np.array(all_losses)

    # Distribution
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    pct_values = np.percentile(all_losses, percentiles)

    print("   Loss distribution:")
    for p, v in zip(percentiles, pct_values):
        print(f"      {p}th percentile: {v:.4f}")

    # Sample low/high loss names
    sorted_indices = np.argsort(all_losses)

    low_loss = [(names[i], all_losses[i], counts[i])
                for i in sorted_indices[:50]]
    high_loss = [(names[i], all_losses[i], counts[i])
                 for i in sorted_indices[-50:]]

    print("\n   Lowest loss (most color-like):")
    for name, loss, count in low_loss[:10]:
        print(f"      '{name}' (loss={loss:.4f}, n={count})")

    print("\n   Highest loss (least color-like):")
    for name, loss, count in high_loss[-10:]:
        print(f"      '{name}' (loss={loss:.4f}, n={count})")

    # Build results
    results = {
        'total_names': len(names),
        'distribution': {
            'mean': float(np.mean(all_losses)),
            'std': float(np.std(all_losses)),
            'min': float(np.min(all_losses)),
            'max': float(np.max(all_losses)),
            'percentiles': {str(p): float(v) for p, v in zip(percentiles, pct_values)}
        },
        'low_loss_samples': [
            {'name': n, 'loss': float(l), 'count': c}
            for n, l, c in low_loss
        ],
        'high_loss_samples': [
            {'name': n, 'loss': float(l), 'count': c}
            for n, l, c in high_loss
        ]
    }

    # Save results
    save_results(results, 'exp3_autoencoder_full_results.json')

    print(f"\n5. Results saved to exp3_autoencoder_full_results.json")

    return results


def main():
    parser = argparse.ArgumentParser(description="Semantic Autoencoder Experiment")
    parser.add_argument('--small-only', action='store_true',
                        help='Run only small-scale test')
    parser.add_argument('--full-only', action='store_true',
                        help='Run only full-scale')
    parser.add_argument('--batch-size', type=int, default=1000,
                        help='Batch size for full-scale')
    args = parser.parse_args()

    if args.full_only:
        run_full_scale(batch_size=args.batch_size)
    else:
        results, model = run_small_scale()

        if not args.small_only:
            run_full_scale(model, args.batch_size)


if __name__ == "__main__":
    main()
