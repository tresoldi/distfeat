#!/usr/bin/env python3
"""Verify all tracked handbook examples.

Runs each example script, captures stdout, compares against the stored
output.txt, and updates meta.txt with verification status.

Usage:
    python scripts/verify_examples.py          # verify all
    python scripts/verify_examples.py ch03     # verify one chapter
    python scripts/verify_examples.py --update # regenerate output.txt
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = PROJECT_ROOT / "docs" / "handbook" / "examples"
SRC_DIR = PROJECT_ROOT / "src"


def find_example_dirs(filter_prefix: str | None = None) -> list[Path]:
    """Find all example directories, optionally filtered by prefix."""
    dirs = sorted(
        d for d in EXAMPLES_DIR.iterdir()
        if d.is_dir() and (d / "run.py").exists()
    )
    if filter_prefix:
        dirs = [d for d in dirs if d.name.startswith(filter_prefix)]
    return dirs


def run_example(example_dir: Path) -> tuple[bool, str, str]:
    """Run an example and return (success, stdout, stderr)."""
    run_py = example_dir / "run.py"
    command_txt = example_dir / "command.txt"

    if command_txt.exists():
        cmd = command_txt.read_text(encoding="utf-8").strip()
    else:
        cmd = f"python {run_py}"

    env = {**__import__("os").environ, "PYTHONPATH": str(SRC_DIR)}

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=example_dir,
            env=env,
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "TIMEOUT: example exceeded 60 seconds"


def verify_example(
    example_dir: Path,
    *,
    update: bool = False,
) -> tuple[str, bool, str]:
    """Verify a single example. Returns (name, passed, message)."""
    name = example_dir.name
    output_txt = example_dir / "output.txt"
    meta_txt = example_dir / "meta.txt"

    success, stdout, stderr = run_example(example_dir)

    if not success:
        status = "FAIL"
        msg = f"execution failed: {stderr.strip()[:200]}"
        meta_txt.write_text(
            f"verified: {_now()}\nstatus: FAIL\nerror: {stderr.strip()[:200]}\n",
            encoding="utf-8",
        )
        return name, False, msg

    if update or not output_txt.exists():
        output_txt.write_text(stdout, encoding="utf-8")
        status = "UPDATED" if update else "GENERATED"
        msg = f"output.txt {status.lower()}"
    else:
        expected = output_txt.read_text(encoding="utf-8")
        if stdout == expected:
            status = "PASS"
            msg = "output matches"
        else:
            status = "DRIFT"
            msg = "output differs from stored output.txt"

    import distfeat

    meta_txt.write_text(
        f"verified: {_now()}\nversion: {distfeat.__version__}\nstatus: {status}\n",
        encoding="utf-8",
    )
    return name, status in {"PASS", "UPDATED", "GENERATED"}, msg


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify handbook examples")
    parser.add_argument(
        "filter",
        nargs="?",
        default=None,
        help="Filter examples by prefix (e.g., 'ch03')",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Regenerate output.txt files",
    )
    args = parser.parse_args()

    dirs = find_example_dirs(args.filter)
    if not dirs:
        suffix = f" matching {args.filter!r}" if args.filter else ""
        print(f"No example directories found{suffix}.")
        sys.exit(1)

    results: list[tuple[str, bool, str]] = []
    for d in dirs:
        name, passed, msg = verify_example(d, update=args.update)
        marker = "PASS" if passed else "FAIL"
        print(f"  [{marker}] {name}: {msg}")
        results.append((name, passed, msg))

    passed = sum(1 for _, p, _ in results if p)
    total = len(results)
    print(f"\n{passed}/{total} examples passed.")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
