"""
Tests for I/O functionality - loading/saving matrices and data.
"""

import pytest
import tempfile
import json
import csv
from pathlib import Path
import numpy as np

from distfeat.io import (
    save_distance_matrix,
    load_distance_matrix,
    export_features,
    import_custom_features,
    save_alignment_results,
    load_cognate_data
)
from distfeat import build_distance_matrix


class TestMatrixIO:
    """Test distance matrix I/O operations."""
    
    def test_save_load_tsv(self):
        """Test saving and loading distance matrices in TSV format."""
        # Create test matrix
        phonemes = ['p', 'b', 't', 'd']
        matrix, labels = build_distance_matrix(phonemes, method='hamming')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tsv', delete=False) as f:
            filename = f.name
        
        try:
            # Save matrix
            save_distance_matrix(matrix, labels, filename, format='tsv')
            
            # Load matrix back
            loaded_matrix, loaded_labels = load_distance_matrix(filename, format='tsv')
            
            # Verify data integrity
            np.testing.assert_array_almost_equal(matrix, loaded_matrix, decimal=6)
            assert labels == loaded_labels
            
        finally:
            Path(filename).unlink(missing_ok=True)
    
    def test_save_load_json(self):
        """Test saving and loading distance matrices in JSON format."""
        # Create test matrix
        phonemes = ['a', 'e', 'i']
        matrix, labels = build_distance_matrix(phonemes, method='euclidean')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
        
        try:
            # Save matrix
            save_distance_matrix(matrix, labels, filename, format='json')
            
            # Load matrix back
            loaded_matrix, loaded_labels = load_distance_matrix(filename, format='json')
            
            # Verify data integrity
            np.testing.assert_array_almost_equal(matrix, loaded_matrix, decimal=6)
            assert labels == loaded_labels
            
        finally:
            Path(filename).unlink(missing_ok=True)
    
    def test_save_load_csv(self):
        """Test saving and loading distance matrices in CSV format."""
        # Create small test matrix
        phonemes = ['p', 'b']
        matrix, labels = build_distance_matrix(phonemes, method='jaccard')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            filename = f.name
        
        try:
            # Save matrix
            save_distance_matrix(matrix, labels, filename, format='csv')
            
            # Load matrix back
            loaded_matrix, loaded_labels = load_distance_matrix(filename, format='csv')
            
            # Verify data integrity
            np.testing.assert_array_almost_equal(matrix, loaded_matrix, decimal=6)
            assert labels == loaded_labels
            
        finally:
            Path(filename).unlink(missing_ok=True)
    
    def test_matrix_metadata(self):
        """Test saving and loading matrices with metadata."""
        phonemes = ['p', 't', 'k']
        matrix, labels = build_distance_matrix(phonemes, method='hamming')
        
        metadata = {
            'method': 'hamming',
            'normalized': True,
            'date_created': '2024-01-01',
            'phoneme_count': len(phonemes),
            'description': 'Test distance matrix'
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
        
        try:
            # Save with metadata
            save_distance_matrix(
                matrix, labels, filename, 
                format='json', metadata=metadata
            )
            
            # Load back
            loaded_matrix, loaded_labels, loaded_metadata = load_distance_matrix(
                filename, format='json', load_metadata=True
            )
            
            # Verify metadata
            assert loaded_metadata is not None
            assert loaded_metadata['method'] == 'hamming'
            assert loaded_metadata['phoneme_count'] == len(phonemes)
            
        finally:
            Path(filename).unlink(missing_ok=True)
    
    def test_large_matrix(self):
        """Test I/O with larger matrices."""
        # Create larger matrix
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'ŋ', 'f', 'v', 's', 'z']
        matrix, labels = build_distance_matrix(phonemes[:10], method='hamming')  # Limit size
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tsv', delete=False) as f:
            filename = f.name
        
        try:
            # Save and load
            save_distance_matrix(matrix, labels, filename, format='tsv')
            loaded_matrix, loaded_labels = load_distance_matrix(filename, format='tsv')
            
            # Verify
            np.testing.assert_array_almost_equal(matrix, loaded_matrix, decimal=6)
            assert labels == loaded_labels
            
        finally:
            Path(filename).unlink(missing_ok=True)


class TestFeatureIO:
    """Test feature system I/O."""
    
    def test_export_features(self):
        """Test exporting phoneme features."""
        phonemes = ['p', 'b', 't', 'd']
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            filename = f.name
        
        try:
            # Export features
            export_features(phonemes, filename, format='csv')
            
            # Verify file exists and has content
            assert Path(filename).exists()
            
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                assert len(content) > 0
                # Should contain phonemes
                for phoneme in phonemes:
                    assert phoneme in content
                    
        finally:
            Path(filename).unlink(missing_ok=True)
    
    def test_import_custom_features(self):
        """Test importing custom feature systems."""
        # Create test feature file
        test_features = [
            ['phoneme', 'consonantal', 'voice', 'labial'],
            ['p', '1', '0', '1'],
            ['b', '1', '1', '1'],
            ['t', '1', '0', '0'],
            ['d', '1', '1', '0'],
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            filename = f.name
            writer = csv.writer(f)
            writer.writerows(test_features)
        
        try:
            # Import custom features
            feature_system = import_custom_features(
                filename, 
                phoneme_col='phoneme',
                delimiter=','
            )
            
            # Verify imported data
            assert isinstance(feature_system, dict)
            assert len(feature_system) == 4  # 4 phonemes
            
            # Check structure
            assert 'p' in feature_system
            assert 'features' in feature_system['p']
            assert feature_system['p']['features']['consonantal'] == 1
            assert feature_system['p']['features']['voice'] == 0
            assert feature_system['p']['features']['labial'] == 1
            
        finally:
            Path(filename).unlink(missing_ok=True)
    
    def test_feature_format_validation(self):
        """Test validation of feature file formats."""
        # Invalid format - missing required columns
        invalid_features = [
            ['sound', 'feature1'],  # Missing 'phoneme' column
            ['p', '1'],
            ['b', '0'],
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            filename = f.name
            writer = csv.writer(f)
            writer.writerows(invalid_features)
        
        try:
            # Should handle gracefully or raise informative error
            with pytest.raises((ValueError, KeyError)):
                import_custom_features(
                    filename,
                    phoneme_col='phoneme',  # Column doesn't exist
                    delimiter=','
                )
                
        finally:
            Path(filename).unlink(missing_ok=True)


class TestAlignmentIO:
    """Test alignment result I/O."""
    
    def test_save_alignment_results(self):
        """Test saving alignment results."""
        # Mock alignment results
        alignment_data = [
            {
                'seq1': ['p', 'a', 't'],
                'seq2': ['b', 'a', 'd'],
                'seq1_aligned': ['p', 'a', 't'],
                'seq2_aligned': ['b', 'a', 'd'],
                'distance': 0.667,
                'method': 'hamming'
            },
            {
                'seq1': ['k', 'a', 't'],
                'seq2': ['g', 'a', 't'],
                'seq1_aligned': ['k', 'a', 't'],
                'seq2_aligned': ['g', 'a', 't'],
                'distance': 0.333,
                'method': 'hamming'
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
        
        try:
            # Save alignment results
            save_alignment_results(alignment_data, filename)
            
            # Verify file exists and has correct structure
            assert Path(filename).exists()
            
            with open(filename, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                
            assert isinstance(loaded_data, list)
            assert len(loaded_data) == 2
            
            # Check first alignment
            first = loaded_data[0]
            assert 'seq1' in first
            assert 'seq2' in first
            assert 'distance' in first
            assert first['distance'] == 0.667
            
        finally:
            Path(filename).unlink(missing_ok=True)


class TestCognateDataIO:
    """Test cognate data loading."""
    
    def test_load_cognate_data(self):
        """Test loading cognate data from CSV."""
        # Create test cognate file
        cognate_data = [
            ['Language', 'Word', 'Segments', 'Cognacy', 'Concept'],
            ['English', 'dog', 'd o g', '1', 'animal'],
            ['German', 'Hund', 'h u n t', '2', 'animal'],
            ['Spanish', 'perro', 'p e r o', '3', 'animal'],
            ['English', 'cat', 'k a t', '4', 'animal'],
            ['German', 'Katze', 'k a t s e', '4', 'animal'],
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            filename = f.name
            writer = csv.writer(f)
            writer.writerows(cognate_data)
        
        try:
            # Load cognate data
            loaded_data = load_cognate_data(filename)
            
            # Verify structure
            assert isinstance(loaded_data, (list, dict))
            
            # Should have processed the data
            if isinstance(loaded_data, list):
                assert len(loaded_data) > 0
            elif isinstance(loaded_data, dict):
                assert len(loaded_data) > 0
                
        finally:
            Path(filename).unlink(missing_ok=True)
    
    def test_cognate_data_validation(self):
        """Test validation of cognate data format."""
        # Invalid cognate file - missing required columns
        invalid_data = [
            ['Word', 'Language'],  # Missing Segments, Cognacy
            ['dog', 'English'],
            ['Hund', 'German'],
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            filename = f.name
            writer = csv.writer(f)
            writer.writerows(invalid_data)
        
        try:
            # Should handle missing columns gracefully
            with pytest.raises((ValueError, KeyError)):
                load_cognate_data(filename, required_columns=['Segments', 'Cognacy'])
                
        finally:
            Path(filename).unlink(missing_ok=True)


class TestIOErrorHandling:
    """Test I/O error handling."""
    
    def test_file_not_found(self):
        """Test handling of missing files."""
        nonexistent_file = "/nonexistent/path/file.tsv"
        
        with pytest.raises(FileNotFoundError):
            load_distance_matrix(nonexistent_file)
    
    def test_invalid_format(self):
        """Test handling of invalid file formats."""
        # Create file with invalid content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            filename = f.name
            f.write("This is not a valid distance matrix file")
        
        try:
            with pytest.raises((ValueError, json.JSONDecodeError, csv.Error)):
                load_distance_matrix(filename, format='json')
                
        finally:
            Path(filename).unlink(missing_ok=True)
    
    def test_corrupted_data(self):
        """Test handling of corrupted data files."""
        # Create partially corrupted JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
            f.write('{"matrix": [[1, 2], [2, 1]], "labels": ["a"')  # Missing closing bracket
        
        try:
            with pytest.raises(json.JSONDecodeError):
                load_distance_matrix(filename, format='json')
                
        finally:
            Path(filename).unlink(missing_ok=True)
    
    def test_permission_errors(self, tmp_path):
        """Test handling of permission errors."""
        # Create file in directory without write permission
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)  # Read-only
        
        try:
            readonly_file = readonly_dir / "matrix.tsv"
            
            phonemes = ['p', 'b']
            matrix, labels = build_distance_matrix(phonemes)
            
            # Should raise PermissionError or similar
            with pytest.raises((PermissionError, OSError)):
                save_distance_matrix(matrix, labels, str(readonly_file))
                
        finally:
            # Restore permissions for cleanup
            readonly_dir.chmod(0o755)