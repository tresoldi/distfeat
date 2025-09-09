"""
Sequence alignment for cognate testing.

This module provides Needleman-Wunsch alignment for evaluating distance metrics
against cognate data. It's used internally for testing and optimization.
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass

from .distances import calculate_distance


@dataclass
class AlignmentResult:
    """Result of sequence alignment."""
    score: float
    seq1_aligned: List[str]
    seq2_aligned: List[str]
    distance: float
    normalized_distance: float
    
    def __str__(self) -> str:
        seq1 = ' '.join(self.seq1_aligned)
        seq2 = ' '.join(self.seq2_aligned)
        return f"Distance: {self.normalized_distance:.3f}\n{seq1}\n{seq2}"


def align_sequences(
    seq1: List[str],
    seq2: List[str],
    method: str = 'hamming',
    gap_penalty: float = 1.0,
    normalize: bool = True
) -> AlignmentResult:
    """
    Align two phonetic sequences using Needleman-Wunsch algorithm.
    
    Args:
        seq1: First sequence of phonemes
        seq2: Second sequence of phonemes
        method: Distance method to use
        gap_penalty: Penalty for gaps
        normalize: Normalize distances
        
    Returns:
        AlignmentResult with aligned sequences and scores
    """
    if not seq1 or not seq2:
        # Handle empty sequences
        if not seq1 and not seq2:
            return AlignmentResult(0.0, [], [], 0.0, 0.0)
        elif not seq1:
            gaps = ['-'] * len(seq2)
            score = len(seq2) * gap_penalty
            return AlignmentResult(score, gaps, seq2, score, score/max(len(seq2), 1))
        else:
            gaps = ['-'] * len(seq1)
            score = len(seq1) * gap_penalty
            return AlignmentResult(score, seq1, gaps, score, score/max(len(seq1), 1))
    
    m, n = len(seq1), len(seq2)
    
    # Initialize DP matrix
    dp = np.zeros((m + 1, n + 1))
    
    # Initialize with gap penalties
    for i in range(1, m + 1):
        dp[i][0] = i * gap_penalty
    for j in range(1, n + 1):
        dp[0][j] = j * gap_penalty
    
    # Fill DP matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate substitution cost
            dist = calculate_distance(
                seq1[i-1], seq2[j-1], 
                method=method, 
                normalize=normalize,
                on_error='ignore'
            )
            if dist is None:
                dist = 1.0 if normalize else 2.0
            
            # Take minimum of three operations
            dp[i][j] = min(
                dp[i-1][j-1] + dist,  # Substitution
                dp[i-1][j] + gap_penalty,  # Deletion
                dp[i][j-1] + gap_penalty   # Insertion
            )
    
    # Traceback to get alignment
    aligned1, aligned2 = [], []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            dist = calculate_distance(
                seq1[i-1], seq2[j-1],
                method=method,
                normalize=normalize,
                on_error='ignore'
            )
            if dist is None:
                dist = 1.0 if normalize else 2.0
            
            if dp[i][j] == dp[i-1][j-1] + dist:
                aligned1.append(seq1[i-1])
                aligned2.append(seq2[j-1])
                i -= 1
                j -= 1
            elif dp[i][j] == dp[i-1][j] + gap_penalty:
                aligned1.append(seq1[i-1])
                aligned2.append('-')
                i -= 1
            else:
                aligned1.append('-')
                aligned2.append(seq2[j-1])
                j -= 1
        elif i > 0:
            aligned1.append(seq1[i-1])
            aligned2.append('-')
            i -= 1
        else:
            aligned1.append('-')
            aligned2.append(seq2[j-1])
            j -= 1
    
    # Reverse alignments
    aligned1.reverse()
    aligned2.reverse()
    
    # Calculate final score
    final_score = dp[m][n]
    normalized_score = final_score / max(m, n)
    
    return AlignmentResult(
        score=final_score,
        seq1_aligned=aligned1,
        seq2_aligned=aligned2,
        distance=final_score,
        normalized_distance=normalized_score
    )


def align_cognate_set(
    cognates: List[List[str]],
    method: str = 'hamming',
    gap_penalty: float = 1.0
) -> float:
    """
    Calculate average pairwise alignment distance within a cognate set.
    
    Args:
        cognates: List of cognate sequences
        method: Distance method
        gap_penalty: Gap penalty
        
    Returns:
        Average normalized distance between cognates
    """
    if len(cognates) < 2:
        return 0.0
    
    distances = []
    
    for i in range(len(cognates)):
        for j in range(i + 1, len(cognates)):
            result = align_sequences(
                cognates[i], cognates[j],
                method=method,
                gap_penalty=gap_penalty
            )
            distances.append(result.normalized_distance)
    
    return np.mean(distances) if distances else 0.0


def optimize_from_cognates(
    cognate_sets: List[List[List[str]]],
    method: str = 'hamming',
    gap_penalty: float = 1.0
) -> Dict[str, float]:
    """
    Optimize distance parameters using cognate data.
    
    This function calculates statistics that can be used to tune
    distance thresholds for better cognate detection.
    
    Args:
        cognate_sets: List of cognate sets, each containing aligned words
        method: Distance method
        gap_penalty: Gap penalty
        
    Returns:
        Dictionary with optimization statistics
    """
    intra_distances = []  # Distances within cognate sets
    inter_distances = []  # Distances between different sets
    
    # Calculate intra-cognate distances
    for cognate_set in cognate_sets:
        if len(cognate_set) >= 2:
            avg_dist = align_cognate_set(cognate_set, method, gap_penalty)
            intra_distances.append(avg_dist)
    
    # Sample inter-cognate distances
    n_samples = min(100, len(cognate_sets) * (len(cognate_sets) - 1) // 2)
    sampled = 0
    
    for i in range(len(cognate_sets)):
        if sampled >= n_samples:
            break
        for j in range(i + 1, len(cognate_sets)):
            if sampled >= n_samples:
                break
            
            # Compare first word from each set
            if cognate_sets[i] and cognate_sets[j]:
                result = align_sequences(
                    cognate_sets[i][0],
                    cognate_sets[j][0],
                    method=method,
                    gap_penalty=gap_penalty
                )
                inter_distances.append(result.normalized_distance)
                sampled += 1
    
    # Calculate statistics
    stats = {
        'mean_intra_distance': np.mean(intra_distances) if intra_distances else 0.0,
        'std_intra_distance': np.std(intra_distances) if intra_distances else 0.0,
        'mean_inter_distance': np.mean(inter_distances) if inter_distances else 1.0,
        'std_inter_distance': np.std(inter_distances) if inter_distances else 0.0,
        'n_cognate_sets': len(cognate_sets),
        'n_intra_pairs': len(intra_distances),
        'n_inter_pairs': len(inter_distances)
    }
    
    # Calculate optimal threshold
    if intra_distances and inter_distances:
        # Use the point that minimizes classification error
        # assuming Gaussian distributions
        mean_intra = stats['mean_intra_distance']
        mean_inter = stats['mean_inter_distance']
        std_intra = stats['std_intra_distance']
        std_inter = stats['std_inter_distance']
        
        # Optimal threshold (equal error rate point)
        if std_intra + std_inter > 0:
            weight = std_inter / (std_intra + std_inter)
            threshold = weight * mean_intra + (1 - weight) * mean_inter
        else:
            threshold = (mean_intra + mean_inter) / 2
        
        stats['optimal_threshold'] = threshold
        stats['separation'] = mean_inter - mean_intra
    
    return stats