#!/usr/bin/env python3
"""Compile the distfeat handbook to HTML, PDF, and EPUB.

Usage:
    python scripts/compile_handbook.py              # all formats
    python scripts/compile_handbook.py html          # HTML only
    python scripts/compile_handbook.py pdf           # PDF only
    python scripts/compile_handbook.py epub          # EPUB only

Outputs:
    site/                           # HTML (MkDocs)
    build/distfeat-handbook.pdf     # PDF (pandoc + xelatex)
    build/distfeat-handbook.epub    # EPUB (pandoc)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HANDBOOK_DIR = PROJECT_ROOT / "docs" / "handbook"
EXAMPLES_DIR = HANDBOOK_DIR / "examples"
BUILD_DIR = PROJECT_ROOT / "build"
SRC_DIR = PROJECT_ROOT / "src"

# Ordered list of markdown files for linear formats (PDF, EPUB).
CHAPTERS = [
    "index.md",
    "part1/index.md",
    "part1/ch01_features_as_theory.md",
    "part1/ch02_from_phonemes_to_bundles.md",
    "part1/ch03_getting_started.md",
    "part2/index.md",
    "part2/ch04_systems_and_representations.md",
    "part2/ch05_queries_and_classes.md",
    "part2/ch06_matrices_and_geometry.md",
    "part2/ch07_distance.md",
    "part3/index.md",
    "part3/ch08_romance_inventory.md",
    "part3/ch09_modeling_lenition.md",
    "reference/index.md",
    "reference/api_reference.md",
    "reference/feature_catalog.md",
    "reference/glossary.md",
    "reference/troubleshooting.md",
    "about/index.md",
    "about/contributing.md",
    "about/changelog.md",
    "about/license.md",
]


def _get_version() -> str:
    """Import distfeat version."""
    sys.path.insert(0, str(SRC_DIR))
    import distfeat
    return distfeat.__version__


def _read_example_file(relative_path: str) -> str:
    """Read an example file and return as a Python code block."""
    path = EXAMPLES_DIR / relative_path
    if not path.exists():
        return f"<!-- Example not found: {relative_path} -->"
    content = path.read_text(encoding="utf-8").rstrip()
    return f"```python\n{content}\n```"


def _read_example_command(example_dir: str) -> str:
    """Read command.txt and return as a bash code block."""
    path = EXAMPLES_DIR / example_dir / "command.txt"
    if not path.exists():
        return f"<!-- Command not found: {example_dir} -->"
    content = path.read_text(encoding="utf-8").strip()
    return f"```bash\n{content}\n```"


def _read_example_output(example_dir: str) -> str:
    """Read output.txt and return as a code block."""
    path = EXAMPLES_DIR / example_dir / "output.txt"
    if not path.exists():
        return f"<!-- Output not found: {example_dir} -->"
    content = path.read_text(encoding="utf-8").rstrip()
    return f"```\n{content}\n```"


def _read_last_verified(example_dir: str) -> str:
    """Read meta.txt and return status string."""
    path = EXAMPLES_DIR / example_dir / "meta.txt"
    if not path.exists():
        return "not yet verified"
    return path.read_text(encoding="utf-8").strip()


def expand_macros(text: str, version: str) -> str:
    """Expand Jinja2-style macros to their resolved content."""
    # {{ version() }}
    text = text.replace("{{ version() }}", version)

    # {{ include_example("...") }}
    text = re.sub(
        r'\{\{\s*include_example\(\s*"([^"]+)"\s*\)\s*\}\}',
        lambda m: _read_example_file(m.group(1)),
        text,
    )
    # {{ example_command("...") }}
    text = re.sub(
        r'\{\{\s*example_command\(\s*"([^"]+)"\s*\)\s*\}\}',
        lambda m: _read_example_command(m.group(1)),
        text,
    )
    # {{ example_output("...") }}
    text = re.sub(
        r'\{\{\s*example_output\(\s*"([^"]+)"\s*\)\s*\}\}',
        lambda m: _read_example_output(m.group(1)),
        text,
    )
    # {{ last_verified("...") }}
    text = re.sub(
        r'\{\{\s*last_verified\(\s*"([^"]+)"\s*\)\s*\}\}',
        lambda m: _read_last_verified(m.group(1)),
        text,
    )
    return text


def strip_mkdocs_extensions(text: str) -> str:
    """Remove MkDocs Material extensions that pandoc doesn't understand."""
    # Remove admonition syntax (!!!  note "Title" ... ) — keep content
    text = re.sub(r'^!!! \w+(?: ".*?")?$', '', text, flags=re.MULTILINE)
    # Remove ??? (collapsible) markers
    text = re.sub(r'^\?\?\?[+]? \w+(?: ".*?")?$', '', text, flags=re.MULTILINE)
    # Remove {.class} attribute annotations
    text = re.sub(r'\{\.[\w-]+\}', '', text)
    return text


def build_combined_markdown(version: str) -> str:
    """Concatenate all chapters with macro expansion into one markdown."""
    parts: list[str] = []
    for chapter_path in CHAPTERS:
        full_path = HANDBOOK_DIR / chapter_path
        if not full_path.exists():
            print(f"  WARNING: missing {chapter_path}")
            continue
        raw = full_path.read_text(encoding="utf-8")
        expanded = expand_macros(raw, version)
        cleaned = strip_mkdocs_extensions(expanded)
        parts.append(cleaned)
        parts.append("\n\n")
    return "\n".join(parts)


def build_html() -> bool:
    """Build HTML using MkDocs."""
    print("Building HTML...")
    env = {**os.environ, "PYTHONPATH": str(SRC_DIR)}
    result = subprocess.run(
        ["mkdocs", "build", "--strict"],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr}")
        return False
    print(f"  HTML built to {PROJECT_ROOT / 'site'}")
    return True


def build_pdf(combined_md: Path) -> bool:
    """Build PDF using pandoc + xelatex."""
    print("Building PDF...")
    output = BUILD_DIR / "distfeat-handbook.pdf"
    cmd = [
        "pandoc",
        str(combined_md),
        "-o", str(output),
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=1in",
        "-V", "documentclass=report",
        "-V", "fontsize=11pt",
        "-V", "mainfont=Liberation Serif",
        "-V", "sansfont=Noto Sans",
        "-V", "monofont=Liberation Mono",
        "--toc",
        "--toc-depth=3",
        "-V", "toc-title=Contents",
        "--highlight-style=tango",
        "-V", "colorlinks=true",
        "-V", "linkcolor=teal",
        "-V", "urlcolor=teal",
        "-f", "markdown+smart",
        "--standalone",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr[:500]}")
        return False
    print(f"  PDF built to {output}")
    return True


def build_epub(combined_md: Path, version: str) -> bool:
    """Build EPUB using pandoc."""
    print("Building EPUB...")
    output = BUILD_DIR / "distfeat-handbook.epub"
    cmd = [
        "pandoc",
        str(combined_md),
        "-o", str(output),
        "--toc",
        "--toc-depth=3",
        "--highlight-style=tango",
        "-f", "markdown+smart",
        "--standalone",
        "--metadata", "title=The distfeat Handbook",
        "--metadata", "author=Tiago Tresoldi",
        "--metadata", "lang=en-US",
        "--metadata",
        (
            "description=A phonological feature system "
            f"for computational historical linguistics (v{version})"
        ),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr[:500]}")
        return False
    print(f"  EPUB built to {output}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile the distfeat handbook")
    parser.add_argument(
        "formats",
        nargs="*",
        default=["html", "pdf", "epub"],
        choices=["html", "pdf", "epub"],
        help="Output formats (default: all)",
    )
    args = parser.parse_args()
    formats = args.formats

    version = _get_version()
    print(f"distfeat {version}")

    BUILD_DIR.mkdir(exist_ok=True)

    results: dict[str, bool] = {}

    # For PDF and EPUB, prepare the combined markdown
    combined_md: Path | None = None
    if "pdf" in formats or "epub" in formats:
        print("Preparing combined markdown...")
        combined = build_combined_markdown(version)
        combined_md = BUILD_DIR / "distfeat-handbook.md"
        combined_md.write_text(combined, encoding="utf-8")
        print(f"  Combined markdown: {combined_md}")

    if "html" in formats:
        results["html"] = build_html()

    if "pdf" in formats and combined_md:
        results["pdf"] = build_pdf(combined_md)

    if "epub" in formats and combined_md:
        results["epub"] = build_epub(combined_md, version)

    # Summary
    print("\n--- Summary ---")
    for fmt, ok in results.items():
        status = "OK" if ok else "FAILED"
        print(f"  {fmt.upper():5s}: {status}")

    if not all(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
