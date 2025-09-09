"""
Input/Output utilities for distance matrices and feature data.

Supports multiple formats: TSV, CSV, JSON, and NumPy arrays.
"""

import csv
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import numpy as np

logger = logging.getLogger('distfeat')


def save_distance_matrix(
    matrix: np.ndarray,
    phonemes: List[str],
    path: Union[str, Path],
    format: str = 'tsv',
    precision: int = 4
) -> None:
    """
    Save distance matrix to file.
    
    Args:
        matrix: Distance matrix as numpy array
        phonemes: List of phoneme labels
        path: Output file path
        format: Output format ('tsv', 'csv', 'json', 'npy')
        precision: Decimal precision for text formats
    """
    path = Path(path)
    
    if format == 'tsv':
        export_matrix_tsv(matrix, phonemes, path, precision)
    elif format == 'csv':
        export_matrix_csv(matrix, phonemes, path, precision)
    elif format == 'json':
        export_matrix_json(matrix, phonemes, path, precision)
    elif format == 'npy':
        # Save as numpy binary with metadata
        np.savez(path, matrix=matrix, phonemes=phonemes)
    else:
        raise ValueError(f"Unknown format: {format}")
    
    logger.info(f"Saved {len(phonemes)}x{len(phonemes)} matrix to {path}")


def load_distance_matrix(
    path: Union[str, Path],
    format: Optional[str] = None
) -> Tuple[np.ndarray, List[str]]:
    """
    Load distance matrix from file.
    
    Args:
        path: Input file path
        format: Input format (auto-detect if None)
        
    Returns:
        Tuple of (matrix, phoneme list)
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Matrix file not found: {path}")
    
    # Auto-detect format from extension
    if format is None:
        suffix = path.suffix.lower()
        if suffix == '.tsv':
            format = 'tsv'
        elif suffix == '.csv':
            format = 'csv'
        elif suffix == '.json':
            format = 'json'
        elif suffix in ['.npy', '.npz']:
            format = 'npy'
        else:
            # Try to detect from content
            format = _detect_format(path)
    
    if format == 'tsv':
        return _load_tsv_matrix(path)
    elif format == 'csv':
        return _load_csv_matrix(path)
    elif format == 'json':
        return _load_json_matrix(path)
    elif format == 'npy':
        return _load_numpy_matrix(path)
    else:
        raise ValueError(f"Cannot load format: {format}")


def export_matrix_tsv(
    matrix: np.ndarray,
    phonemes: List[str],
    path: Union[str, Path],
    precision: int = 4
) -> None:
    """
    Export matrix in TSV format (UNIPA compatible).
    
    Format:
        <tab>phoneme1<tab>phoneme2<tab>...
        phoneme1<tab>0.0000<tab>0.1234<tab>...
        phoneme2<tab>0.1234<tab>0.0000<tab>...
    """
    path = Path(path)
    
    with open(path, 'w', encoding='utf-8') as f:
        # Write header
        f.write('\t' + '\t'.join(phonemes) + '\n')
        
        # Write rows
        for i, phoneme in enumerate(phonemes):
            row = [phoneme]
            for j in range(len(phonemes)):
                row.append(f'{matrix[i, j]:.{precision}f}')
            f.write('\t'.join(row) + '\n')


def export_matrix_csv(
    matrix: np.ndarray,
    phonemes: List[str],
    path: Union[str, Path],
    precision: int = 4
) -> None:
    """Export matrix in CSV format."""
    path = Path(path)
    
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([''] + phonemes)
        
        # Write rows
        for i, phoneme in enumerate(phonemes):
            row = [phoneme]
            for j in range(len(phonemes)):
                row.append(f'{matrix[i, j]:.{precision}f}')
            writer.writerow(row)


def export_matrix_json(
    matrix: np.ndarray,
    phonemes: List[str],
    path: Union[str, Path],
    precision: int = 4
) -> None:
    """
    Export matrix in JSON format.
    
    Format:
    {
        "phonemes": ["a", "b", ...],
        "matrix": [[0.0, 0.1, ...], ...],
        "metadata": {"size": n, "symmetric": true}
    }
    """
    path = Path(path)
    
    # Check if matrix is symmetric
    is_symmetric = np.allclose(matrix, matrix.T)
    
    # Convert to list with proper precision
    matrix_list = []
    for row in matrix:
        matrix_list.append([round(float(x), precision) for x in row])
    
    data = {
        'phonemes': phonemes,
        'matrix': matrix_list,
        'metadata': {
            'size': len(phonemes),
            'symmetric': is_symmetric,
            'min': float(np.min(matrix)),
            'max': float(np.max(matrix)),
            'mean': float(np.mean(matrix))
        }
    }
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _load_tsv_matrix(path: Path) -> Tuple[np.ndarray, List[str]]:
    """Load TSV format matrix."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines:
        raise ValueError("Empty matrix file")
    
    # Parse header
    header = lines[0].strip().split('\t')
    if header[0] == '':
        phonemes = header[1:]
    else:
        phonemes = header
    
    n = len(phonemes)
    matrix = np.zeros((n, n))
    
    # Parse data rows
    for i, line in enumerate(lines[1:n+1]):
        parts = line.strip().split('\t')
        # Skip phoneme label in first column
        values = parts[1:n+1] if len(parts) > n else parts[:n]
        
        for j, val in enumerate(values):
            try:
                matrix[i, j] = float(val)
            except (ValueError, IndexError):
                matrix[i, j] = 0.0
    
    return matrix, phonemes


def _load_csv_matrix(path: Path) -> Tuple[np.ndarray, List[str]]:
    """Load CSV format matrix."""
    with open(path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        lines = list(reader)
    
    if not lines:
        raise ValueError("Empty matrix file")
    
    # Parse header
    header = lines[0]
    if header[0] == '':
        phonemes = header[1:]
    else:
        phonemes = header
    
    n = len(phonemes)
    matrix = np.zeros((n, n))
    
    # Parse data rows
    for i, row in enumerate(lines[1:n+1]):
        # Skip phoneme label in first column
        values = row[1:n+1] if len(row) > n else row[:n]
        
        for j, val in enumerate(values):
            try:
                matrix[i, j] = float(val)
            except (ValueError, IndexError):
                matrix[i, j] = 0.0
    
    return matrix, phonemes


def _load_json_matrix(path: Path) -> Tuple[np.ndarray, List[str]]:
    """Load JSON format matrix."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    phonemes = data['phonemes']
    matrix = np.array(data['matrix'])
    
    return matrix, phonemes


def _load_numpy_matrix(path: Path) -> Tuple[np.ndarray, List[str]]:
    """Load NumPy format matrix."""
    data = np.load(path)
    
    if isinstance(data, np.ndarray):
        # Old format - just matrix, generate phoneme labels
        matrix = data
        phonemes = [f'p{i}' for i in range(len(matrix))]
    else:
        # New format with metadata
        matrix = data['matrix']
        phonemes = list(data['phonemes'])
    
    return matrix, phonemes


def _detect_format(path: Path) -> str:
    """Try to detect file format from content."""
    with open(path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
    
    if '\t' in first_line:
        return 'tsv'
    elif ',' in first_line:
        return 'csv'
    elif first_line.strip().startswith('{'):
        return 'json'
    else:
        # Try as numpy
        try:
            np.load(path)
            return 'npy'
        except:
            raise ValueError(f"Cannot detect format of {path}")