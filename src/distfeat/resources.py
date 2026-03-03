"""Low-level TSV resource loading for distfeat."""

from __future__ import annotations

import csv
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from distfeat.dataset import FeatureDataset


_DATA_DIR = Path(__file__).resolve().parent / "data"


def _read_tsv(path: Path) -> list[dict[str, str]]:
    """Read a TSV file into a list of dict rows."""
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader)


def _ensure_exists(path: Path) -> None:
    """Raise a clear error if a required TSV file is missing."""
    if not path.is_file():
        msg = f"Required TSV file not found: {path}"
        raise FileNotFoundError(msg)


def _resolve_paths(
    directory: str | Path | None = None,
    *,
    sounds_path: str | Path | None = None,
    classes_path: str | Path | None = None,
    features_path: str | Path | None = None,
) -> tuple[Path, Path, Path]:
    """Resolve the three required TSV paths."""
    if directory is not None:
        base = Path(directory)
        resolved_sounds = base / "sounds.tsv"
        resolved_classes = base / "classes.tsv"
        resolved_features = base / "features.tsv"
    else:
        resolved_sounds = (
            Path(sounds_path) if sounds_path is not None else _DATA_DIR / "sounds.tsv"
        )
        resolved_classes = (
            Path(classes_path) if classes_path is not None else _DATA_DIR / "classes.tsv"
        )
        resolved_features = (
            Path(features_path) if features_path is not None else _DATA_DIR / "features.tsv"
        )

    _ensure_exists(resolved_sounds)
    _ensure_exists(resolved_classes)
    _ensure_exists(resolved_features)
    return resolved_sounds, resolved_classes, resolved_features


@cache
def load_builtin_dataset() -> FeatureDataset:
    """Load the bundled dataset."""
    return load_dataset()


def load_dataset(
    directory: str | Path | None = None,
    *,
    sounds_path: str | Path | None = None,
    classes_path: str | Path | None = None,
    features_path: str | Path | None = None,
) -> FeatureDataset:
    """Load a dataset from package data, a directory, or explicit file paths."""
    from distfeat.dataset import FeatureDataset

    sounds_file, classes_file, features_file = _resolve_paths(
        directory=directory,
        sounds_path=sounds_path,
        classes_path=classes_path,
        features_path=features_path,
    )

    sounds_rows = _read_tsv(sounds_file)
    classes_rows = _read_tsv(classes_file)
    features_rows = _read_tsv(features_file)

    sounds = {row["GRAPHEME"]: row["NAME"] for row in sounds_rows}
    classes = {
        row["SOUND_CLASS"]: (
            row["DESCRIPTION"],
            row["FEATURES"],
            row["GRAPHEMES"].split("|") if row["GRAPHEMES"] else [],
        )
        for row in classes_rows
    }
    features = [(row["VALUE"], row["FEATURE"]) for row in features_rows]

    return FeatureDataset(sounds=sounds, classes=classes, features=features)
