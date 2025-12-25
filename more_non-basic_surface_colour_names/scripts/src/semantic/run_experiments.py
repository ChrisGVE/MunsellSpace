#!/usr/bin/env python3
"""
Master experiment runner for semantic color name investigation.

Runs all experiments in sequence, with options for small-scale testing
or full-scale background execution.
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
VENV_PYTHON = SCRIPT_DIR.parent.parent / ".venv" / "bin" / "python"


def run_experiment(script: str, args: list = None, background: bool = False):
    """Run an experiment script."""
    script_path = SCRIPT_DIR / script
    cmd = [str(VENV_PYTHON), str(script_path)]
    if args:
        cmd.extend(args)

    print(f"\n{'=' * 70}")
    print(f"Running: {' '.join(cmd)}")
    print('=' * 70)

    if background:
        log_file = SCRIPT_DIR / f"{script.replace('.py', '')}_output.log"
        with open(log_file, 'w') as f:
            proc = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT)
        print(f"Started in background, PID: {proc.pid}")
        print(f"Log file: {log_file}")
        return proc
    else:
        result = subprocess.run(cmd, capture_output=False)
        return result.returncode


def run_small_scale():
    """Run all experiments on small test sets."""
    print("\n" + "=" * 70)
    print("SMALL-SCALE EXPERIMENT RUN")
    print("=" * 70)

    start_time = time.time()

    experiments = [
        ("exp1_sbert_similarity.py", ["--small-only"]),
        ("exp2_bert_tokens.py", ["--small-only"]),
        ("exp3_autoencoder.py", ["--small-only"]),
        ("exp5_spelling_preprocess.py", ["--sample-size", "1000"]),
    ]

    for script, args in experiments:
        print(f"\n>>> Running {script}...")
        result = run_experiment(script, args)
        if result != 0:
            print(f"Warning: {script} exited with code {result}")

    total_time = time.time() - start_time
    print(f"\n{'=' * 70}")
    print(f"Small-scale run complete in {total_time:.1f} seconds")
    print("=" * 70)


def run_full_scale(background: bool = False):
    """Run all experiments on full datasets."""
    print("\n" + "=" * 70)
    print("FULL-SCALE EXPERIMENT RUN")
    print("=" * 70)

    if background:
        print("\nStarting experiments in background...")
        procs = []

        experiments = [
            ("exp1_sbert_similarity.py", []),
            ("exp2_bert_tokens.py", []),
            ("exp3_autoencoder.py", []),
            ("exp5_spelling_preprocess.py", ["--full"]),
        ]

        for script, args in experiments:
            proc = run_experiment(script, args, background=True)
            procs.append((script, proc))
            time.sleep(2)  # Stagger starts

        print("\n" + "=" * 70)
        print("Background processes started:")
        for script, proc in procs:
            print(f"  - {script}: PID {proc.pid}")
        print("\nMonitor with: tail -f overlay-preprocessing/semantic-investigation/*_output.log")
        print("=" * 70)

    else:
        start_time = time.time()

        experiments = [
            ("exp1_sbert_similarity.py", []),
            ("exp2_bert_tokens.py", []),
            ("exp3_autoencoder.py", []),
            ("exp5_spelling_preprocess.py", ["--full"]),
            ("exp4_hybrid.py", []),  # Run after 1 and 3
        ]

        for script, args in experiments:
            print(f"\n>>> Running {script}...")
            result = run_experiment(script, args)
            if result != 0:
                print(f"Warning: {script} exited with code {result}")

        total_time = time.time() - start_time
        print(f"\n{'=' * 70}")
        print(f"Full-scale run complete in {total_time/60:.1f} minutes")
        print("=" * 70)


def check_status():
    """Check status of background jobs."""
    import os
    import signal

    log_files = list(SCRIPT_DIR.glob("*_output.log"))

    print("\n" + "=" * 70)
    print("EXPERIMENT STATUS")
    print("=" * 70)

    for log_file in sorted(log_files):
        print(f"\n{log_file.name}:")

        # Get last few lines
        with open(log_file) as f:
            lines = f.readlines()
            if lines:
                print("  Last output:")
                for line in lines[-5:]:
                    print(f"    {line.rstrip()}")
            else:
                print("  (empty)")


def main():
    parser = argparse.ArgumentParser(description="Run semantic experiments")
    parser.add_argument('mode', choices=['small', 'full', 'background', 'status'],
                        help='Run mode: small (test), full (all data), '
                             'background (full in background), status (check progress)')
    args = parser.parse_args()

    if args.mode == 'small':
        run_small_scale()
    elif args.mode == 'full':
        run_full_scale(background=False)
    elif args.mode == 'background':
        run_full_scale(background=True)
    elif args.mode == 'status':
        check_status()


if __name__ == "__main__":
    main()
