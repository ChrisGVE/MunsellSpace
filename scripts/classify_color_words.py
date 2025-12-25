#!/usr/bin/env python3
"""
Color Word Classification: Statistical vs ML Comparison

Compares two methods for identifying color words:
1. Statistical: Hue variance threshold
2. ML: Classifier trained on known color terms vs modifiers

Training data:
- Positive: Centore 20 overlays + ISCC-NBS basic terms
- Negative: Known modifiers (light, dark, bright, etc.)
"""

import json
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

INPUT_FILE = Path("tmp/xkcd_word_analysis.json")
OUTPUT_FILE = Path("tmp/classification_comparison.json")

# Ground truth: Known color terms
CENTORE_OVERLAYS = {
    'aqua', 'beige', 'coral', 'fuchsia', 'gold', 'lavender', 'lilac',
    'magenta', 'mauve', 'navy', 'peach', 'rose', 'rust', 'sand',
    'tan', 'taupe', 'teal', 'turquoise', 'violet', 'wine'
}

ISCC_NBS_BASIC = {
    'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink',
    'brown', 'olive', 'white', 'gray', 'black'
}

# Additional known color terms (not modifiers)
ADDITIONAL_COLORS = {
    'maroon', 'salmon', 'mustard', 'mint', 'seafoam', 'plum', 'burgundy',
    'cream', 'ivory', 'charcoal', 'slate', 'indigo', 'cyan', 'lime',
    'periwinkle', 'khaki', 'crimson', 'scarlet', 'azure', 'cerulean',
    'chartreuse', 'vermilion', 'ochre', 'sienna', 'umber', 'sepia'
}

KNOWN_COLORS = CENTORE_OVERLAYS | ISCC_NBS_BASIC | ADDITIONAL_COLORS

# Known modifiers (not color terms)
KNOWN_MODIFIERS = {
    'light', 'dark', 'bright', 'pale', 'deep', 'vivid', 'dull',
    'muted', 'soft', 'hard', 'warm', 'cool', 'hot', 'cold',
    'neon', 'pastel', 'dusty', 'dirty', 'faded', 'washed',
    'pure', 'true', 'rich', 'intense', 'subtle', 'medium',
    'very', 'extra', 'ultra', 'super', 'ish', 'ish',
    'grayish', 'greyish', 'greenish', 'bluish', 'reddish', 'yellowish',
    'pinkish', 'brownish', 'purplish', 'orangish', 'blackish', 'whitish',
    'lighter', 'darker', 'brighter', 'duller', 'off', 'almost'
}


def extract_features(word_stat):
    """Extract numeric features from word statistics."""
    return [
        word_stat.get('hue_std', 100) or 100,  # Hue standard deviation
        word_stat.get('sat_mean', 0.5) or 0.5,  # Mean saturation
        word_stat.get('sat_std', 0.3) or 0.3,   # Saturation std
        word_stat.get('val_mean', 0.5) or 0.5,  # Mean value (brightness)
        word_stat.get('val_std', 0.2) or 0.2,   # Value std
        word_stat.get('num_colors', 1),          # Number of color variants
        len(word_stat.get('word', '')),          # Word length
    ]


def main():
    print("Loading word analysis data...")
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    all_words = data['color_words'] + data['modifiers'] + data['ambiguous']
    word_dict = {w['word']: w for w in all_words}

    print(f"  Total words: {len(all_words)}")

    # Build training data from known labels
    X_train = []
    y_train = []
    train_words = []

    for word, ws in word_dict.items():
        if word in KNOWN_COLORS:
            X_train.append(extract_features(ws))
            y_train.append(1)  # Color term
            train_words.append(word)
        elif word in KNOWN_MODIFIERS:
            X_train.append(extract_features(ws))
            y_train.append(0)  # Modifier
            train_words.append(word)

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    print(f"\nTraining data:")
    print(f"  Color terms (positive): {sum(y_train)}")
    print(f"  Modifiers (negative): {len(y_train) - sum(y_train)}")

    # Train classifier
    print("\nTraining Random Forest classifier...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    clf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    clf.fit(X_train_scaled, y_train)

    # Cross-validation
    cv_scores = cross_val_score(clf, X_train_scaled, y_train, cv=5)
    print(f"  Cross-validation accuracy: {cv_scores.mean():.2%} (±{cv_scores.std():.2%})")

    # Feature importance
    feature_names = ['hue_std', 'sat_mean', 'sat_std', 'val_mean', 'val_std', 'num_colors', 'word_len']
    importances = clf.feature_importances_
    print("\n  Feature importance:")
    for name, imp in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
        print(f"    {name:12}: {imp:.3f}")

    # Predict on all words
    print("\nClassifying all words...")
    X_all = np.array([extract_features(ws) for ws in all_words])
    X_all_scaled = scaler.transform(X_all)
    predictions = clf.predict(X_all_scaled)
    probabilities = clf.predict_proba(X_all_scaled)[:, 1]  # Probability of being a color term

    # Compare with statistical method
    print("\n" + "=" * 90)
    print("COMPARISON: Statistical (Hue Variance) vs ML (Random Forest)")
    print("=" * 90)

    # Categorize results
    stat_color = set(w['word'] for w in data['color_words'])
    stat_modifier = set(w['word'] for w in data['modifiers'])
    stat_ambiguous = set(w['word'] for w in data['ambiguous'])

    ml_color = set()
    ml_modifier = set()
    for ws, pred, prob in zip(all_words, predictions, probabilities):
        if pred == 1:
            ml_color.add(ws['word'])
        else:
            ml_modifier.add(ws['word'])

    # Agreement analysis
    both_color = stat_color & ml_color
    both_modifier = stat_modifier & ml_modifier
    stat_only_color = stat_color - ml_color
    ml_only_color = ml_color - stat_color
    disagreement = (stat_color & ml_modifier) | (stat_modifier & ml_color)

    print(f"\nAgreement Summary:")
    print(f"  Both say COLOR:    {len(both_color):3} words")
    print(f"  Both say MODIFIER: {len(both_modifier):3} words")
    print(f"  Statistical only:  {len(stat_only_color):3} words classified as color")
    print(f"  ML only:           {len(ml_only_color):3} words classified as color")
    print(f"  Disagreements:     {len(disagreement):3} words")

    # Show disagreements
    print("\n" + "-" * 90)
    print("DISAGREEMENTS (Statistical says one thing, ML says another)")
    print("-" * 90)

    disagreement_details = []
    for ws in all_words:
        word = ws['word']
        stat_class = 'color' if word in stat_color else ('modifier' if word in stat_modifier else 'ambiguous')
        ml_class = 'color' if word in ml_color else 'modifier'
        prob = probabilities[all_words.index(ws)]

        if stat_class != ml_class and stat_class != 'ambiguous':
            hue_std = ws.get('hue_std')
            hue_std_str = f"{hue_std:.0f}°" if hue_std else "N/A"
            disagreement_details.append({
                'word': word,
                'stat': stat_class,
                'ml': ml_class,
                'ml_prob': prob,
                'hue_std': hue_std,
                'responses': ws['total_responses']
            })

    disagreement_details.sort(key=lambda x: x['responses'], reverse=True)
    for d in disagreement_details[:25]:
        hue_str = f"{d['hue_std']:.0f}°" if d['hue_std'] else "N/A"
        print(f"  {d['word']:20} stat={d['stat']:8} ml={d['ml']:8} "
              f"(prob={d['ml_prob']:.2f}, hue_std={hue_str:>5}, {d['responses']:>7,} resp)")

    # Show ambiguous words resolved by ML
    print("\n" + "-" * 90)
    print("AMBIGUOUS (Statistical) - ML Classification")
    print("-" * 90)

    for ws in data['ambiguous']:
        word = ws['word']
        idx = [w['word'] for w in all_words].index(word)
        prob = probabilities[idx]
        ml_class = 'COLOR' if predictions[idx] == 1 else 'modifier'
        hue_std = ws.get('hue_std')
        hue_str = f"{hue_std:.0f}°" if hue_std else "N/A"
        print(f"  {word:20} -> {ml_class:8} (prob={prob:.2f}, hue_std={hue_str:>5}, {ws['total_responses']:>7,} resp)")

    # New overlay candidates (high confidence from both methods)
    print("\n" + "=" * 90)
    print("HIGH CONFIDENCE NEW OVERLAY CANDIDATES (Both methods agree: COLOR)")
    print("=" * 90)

    # Exclude basic ISCC-NBS terms and Centore overlays
    existing = CENTORE_OVERLAYS | ISCC_NBS_BASIC
    new_candidates = []

    for ws in all_words:
        word = ws['word']
        if word in existing:
            continue

        idx = [w['word'] for w in all_words].index(word)
        prob = probabilities[idx]

        # Both methods agree it's a color AND high ML confidence
        if word in stat_color and word in ml_color and prob > 0.7:
            new_candidates.append({
                'word': word,
                'responses': ws['total_responses'],
                'hue_mean': ws.get('hue_mean'),
                'hue_std': ws.get('hue_std'),
                'ml_prob': prob,
                'hex': ws.get('hex', '#000000')
            })

    new_candidates.sort(key=lambda x: x['responses'], reverse=True)

    print(f"\nFound {len(new_candidates)} new overlay candidates:\n")
    for c in new_candidates[:30]:
        hue_str = f"{c['hue_mean']:.0f}°" if c['hue_mean'] else "N/A"
        std_str = f"±{c['hue_std']:.0f}°" if c['hue_std'] else ""
        print(f"  {c['word']:20} {c['responses']:>8,} resp  hue: {hue_str:>5} {std_str:>5}  "
              f"prob: {c['ml_prob']:.2f}  {c['hex']}")

    # Save results
    print(f"\nSaving comparison results to {OUTPUT_FILE}...")
    output = {
        'cv_accuracy': float(cv_scores.mean()),
        'feature_importances': dict(zip(feature_names, [float(x) for x in importances])),
        'agreement': {
            'both_color': list(both_color),
            'both_modifier': list(both_modifier),
            'stat_only_color': list(stat_only_color),
            'ml_only_color': list(ml_only_color)
        },
        'disagreements': disagreement_details,
        'new_candidates': new_candidates
    }
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print("\nDone!")


if __name__ == "__main__":
    main()
