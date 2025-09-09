"""
Performance and benchmark tests for distfeat.
"""

import pytest
import time
import numpy as np
from memory_profiler import profile
from distfeat import (
    phoneme_to_features,
    calculate_distance,
    build_distance_matrix,
    available_distance_methods
)


class TestPerformanceBenchmarks:
    """Benchmark performance of core functions."""
    
    def test_feature_lookup_performance(self):
        """Benchmark phoneme feature lookup performance."""
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'ŋ', 'f', 'v', 's', 'z']
        
        # Cold start timing
        phoneme_to_features.cache_clear()
        
        start_time = time.time()
        for _ in range(100):
            for phoneme in phonemes:
                phoneme_to_features(phoneme)
        cold_time = time.time() - start_time
        
        # Warm cache timing
        start_time = time.time()
        for _ in range(100):
            for phoneme in phonemes:
                phoneme_to_features(phoneme)
        warm_time = time.time() - start_time
        
        # Cache should provide significant speedup
        speedup = cold_time / warm_time
        assert speedup > 2.0, f"Cache speedup too low: {speedup:.1f}x"
        
        print(f"Feature lookup speedup: {speedup:.1f}x")
    
    def test_distance_calculation_performance(self):
        """Benchmark distance calculation performance."""
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n']
        methods = ['hamming', 'jaccard', 'euclidean']
        
        # Time each method
        timings = {}
        for method in methods:
            start_time = time.time()
            
            for _ in range(50):
                for i in range(len(phonemes)):
                    for j in range(i + 1, len(phonemes)):
                        calculate_distance(phonemes[i], phonemes[j], method=method)
            
            elapsed = time.time() - start_time
            timings[method] = elapsed
            
            # Should complete reasonably quickly
            assert elapsed < 5.0, f"Method {method} too slow: {elapsed:.2f}s"
        
        print("Distance calculation timings:", timings)
    
    def test_matrix_building_performance(self):
        """Benchmark distance matrix construction."""
        test_sizes = [5, 10, 20, 30]
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'ŋ', 'f', 
                   'v', 's', 'z', 'ʃ', 'ʒ', 'x', 'ɣ', 'h', 'l', 'r',
                   'a', 'e', 'i', 'o', 'u', 'ə', 'ɪ', 'ʊ', 'æ', 'ʌ']
        
        timings = []
        
        for size in test_sizes:
            if size <= len(phonemes):
                test_phonemes = phonemes[:size]
                
                start_time = time.time()
                matrix, labels = build_distance_matrix(test_phonemes, method='hamming')
                elapsed = time.time() - start_time
                
                timings.append((size, elapsed))
                
                # Verify matrix properties
                assert matrix.shape == (size, size)
                assert len(labels) == size
                
                print(f"Matrix size {size}x{size}: {elapsed:.3f}s")
        
        # Check that timing grows reasonably with size
        if len(timings) >= 2:
            # Should not be exponential growth
            small_time = timings[0][1]
            large_time = timings[-1][1]
            size_ratio = timings[-1][0] / timings[0][0]
            time_ratio = large_time / small_time
            
            # Time should grow roughly quadratically or less
            assert time_ratio <= size_ratio ** 2.5, \
                f"Performance degradation too severe: {time_ratio:.1f}x for {size_ratio:.1f}x size"
    
    def test_cache_efficiency(self):
        """Test LRU cache efficiency."""
        # Clear cache
        calculate_distance.cache_clear()
        
        # Fill cache with unique calculations
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'ŋ', 'f']
        for i in range(len(phonemes)):
            for j in range(i + 1, len(phonemes)):
                calculate_distance(phonemes[i], phonemes[j])
        
        # Get cache info
        cache_info = calculate_distance.cache_info()
        
        # Should have good hit rate after warming up
        if cache_info.hits + cache_info.misses > 0:
            hit_rate = cache_info.hits / (cache_info.hits + cache_info.misses)
            print(f"Cache hit rate: {hit_rate:.2%}")
            
        # Cache should be used efficiently
        assert cache_info.currsize > 0, "Cache not being used"
        assert cache_info.currsize <= cache_info.maxsize, "Cache overflow"
    
    def test_memory_usage(self):
        """Test memory usage of distance matrix construction."""
        # This is a basic test - full memory profiling needs memory_profiler
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'ŋ', 'f']
        
        # Build matrix
        matrix, labels = build_distance_matrix(phonemes)
        
        # Check matrix size in memory
        matrix_size_mb = matrix.nbytes / (1024 * 1024)
        print(f"Matrix memory usage: {matrix_size_mb:.3f} MB")
        
        # Should be reasonable for small matrices
        assert matrix_size_mb < 1.0, f"Memory usage too high: {matrix_size_mb:.3f} MB"


class TestScalabilityLimits:
    """Test scalability and find performance limits."""
    
    def test_large_phoneme_set(self):
        """Test with larger phoneme sets."""
        # Create large phoneme list (subset of actual phonemes)
        large_phoneme_set = [
            'p', 'b', 't', 'd', 'k', 'g', 'q', 'ɢ', 'm', 'n', 'ɲ', 'ŋ', 'ɴ',
            'ʙ', 'r', 'ɾ', 'ʀ', 'ɸ', 'β', 'f', 'v', 'θ', 'ð', 's', 'z',
            'ʃ', 'ʒ', 'ʂ', 'ʐ', 'ç', 'ʝ', 'x', 'ɣ', 'χ', 'ʁ', 'ħ', 'ʕ',
            'h', 'ɦ', 'l', 'ɭ', 'ʎ', 'ʟ', 'ɬ', 'ɮ', 'ʋ', 'ɹ', 'ɻ', 'j',
        ][:25]  # Limit to manageable size
        
        # Test matrix construction time
        start_time = time.time()
        matrix, labels = build_distance_matrix(large_phoneme_set, method='hamming')
        elapsed = time.time() - start_time
        
        print(f"Large set ({len(large_phoneme_set)} phonemes): {elapsed:.2f}s")
        
        # Should complete within reasonable time
        assert elapsed < 30.0, f"Large set too slow: {elapsed:.2f}s"
        
        # Verify correctness
        assert matrix.shape == (len(large_phoneme_set), len(large_phoneme_set))
        assert np.allclose(matrix, matrix.T)  # Symmetric
        assert np.allclose(np.diag(matrix), 0)  # Zero diagonal
    
    def test_method_comparison_performance(self):
        """Compare performance of different distance methods."""
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'ŋ', 'f']
        methods = available_distance_methods()
        
        # Filter to core methods for performance comparison
        core_methods = [m for m in methods if m in ['hamming', 'jaccard', 'euclidean', 'cosine', 'manhattan']]
        
        method_timings = {}
        
        for method in core_methods:
            start_time = time.time()
            
            matrix, labels = build_distance_matrix(phonemes, method=method)
            
            elapsed = time.time() - start_time
            method_timings[method] = elapsed
            
            print(f"Method {method}: {elapsed:.3f}s")
        
        # Find fastest method
        if method_timings:
            fastest_method = min(method_timings.items(), key=lambda x: x[1])
            print(f"Fastest method: {fastest_method[0]} ({fastest_method[1]:.3f}s)")
        
        # All methods should complete reasonably quickly
        for method, timing in method_timings.items():
            assert timing < 5.0, f"Method {method} too slow: {timing:.3f}s"
    
    def test_concurrent_access(self):
        """Test performance with concurrent access (threading)."""
        import threading
        import queue
        
        phonemes = ['p', 'b', 't', 'd', 'k', 'g']
        results = queue.Queue()
        
        def worker():
            """Worker thread for distance calculations."""
            local_results = []
            for i in range(10):
                for p1 in phonemes:
                    for p2 in phonemes:
                        if p1 != p2:
                            dist = calculate_distance(p1, p2)
                            local_results.append(dist)
            results.put(local_results)
        
        # Start multiple threads
        threads = []
        num_threads = 4
        
        start_time = time.time()
        
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        elapsed = time.time() - start_time
        
        # Collect results
        all_results = []
        while not results.empty():
            thread_results = results.get()
            all_results.extend(thread_results)
        
        print(f"Concurrent access ({num_threads} threads): {elapsed:.3f}s")
        
        # Should complete and return consistent results
        assert len(all_results) > 0
        assert elapsed < 10.0, f"Concurrent access too slow: {elapsed:.3f}s"


class TestMemoryEfficiency:
    """Test memory usage and efficiency."""
    
    def test_matrix_memory_scaling(self):
        """Test memory usage scaling with matrix size."""
        sizes = [5, 10, 15, 20]
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'ŋ', 'f', 
                   'v', 's', 'z', 'ʃ', 'ʒ', 'x', 'ɣ', 'h', 'l', 'r']
        
        memory_usage = []
        
        for size in sizes:
            if size <= len(phonemes):
                matrix, _ = build_distance_matrix(phonemes[:size])
                size_mb = matrix.nbytes / (1024 * 1024)
                memory_usage.append((size, size_mb))
                
                print(f"Size {size}: {size_mb:.3f} MB")
        
        # Memory should scale quadratically (O(n²))
        if len(memory_usage) >= 2:
            for i in range(1, len(memory_usage)):
                size_ratio = memory_usage[i][0] / memory_usage[0][0]
                memory_ratio = memory_usage[i][1] / memory_usage[0][1]
                
                # Should be roughly quadratic
                expected_ratio = size_ratio ** 2
                assert memory_ratio <= expected_ratio * 1.2, \
                    f"Memory scaling worse than expected: {memory_ratio:.1f}x vs {expected_ratio:.1f}x"
    
    def test_cache_memory_limit(self):
        """Test that cache doesn't exceed memory limits."""
        # Generate many unique distance calculations
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'ŋ', 'f', 'v', 's', 'z']
        
        # Clear cache
        calculate_distance.cache_clear()
        
        # Fill cache beyond its limit
        calculation_count = 0
        for i in range(len(phonemes)):
            for j in range(len(phonemes)):
                if i != j:
                    calculate_distance(phonemes[i], phonemes[j])
                    calculation_count += 1
        
        cache_info = calculate_distance.cache_info()
        
        # Cache should respect its size limit
        assert cache_info.currsize <= cache_info.maxsize, \
            f"Cache exceeded limit: {cache_info.currsize} > {cache_info.maxsize}"
        
        print(f"Generated {calculation_count} calculations, cache size: {cache_info.currsize}")
        
        # Should have some cache evictions if we exceeded the limit
        if calculation_count > cache_info.maxsize:
            assert cache_info.currsize == cache_info.maxsize, \
                "Cache should be at maximum size after overflow"


class TestPerformanceRegression:
    """Test for performance regressions."""
    
    def test_baseline_performance(self):
        """Establish baseline performance metrics."""
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n']
        
        # Single distance calculation
        start = time.time()
        for _ in range(1000):
            calculate_distance('p', 'b')
        single_calc_time = time.time() - start
        
        # Matrix building
        start = time.time()
        build_distance_matrix(phonemes)
        matrix_time = time.time() - start
        
        print(f"Baseline metrics:")
        print(f"  1000 distance calculations: {single_calc_time:.3f}s")
        print(f"  8x8 matrix building: {matrix_time:.3f}s")
        
        # Set reasonable performance thresholds
        assert single_calc_time < 1.0, f"Distance calc too slow: {single_calc_time:.3f}s"
        assert matrix_time < 2.0, f"Matrix building too slow: {matrix_time:.3f}s"
    
    @pytest.mark.slow
    def test_stress_test(self):
        """Stress test with intensive operations."""
        # This test might be skipped in regular runs
        phonemes = ['p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'ŋ', 'f', 'v', 's']
        methods = ['hamming', 'euclidean', 'jaccard']
        
        start_time = time.time()
        
        # Build multiple large matrices
        for method in methods:
            matrix, _ = build_distance_matrix(phonemes, method=method)
            
            # Verify matrix quality
            assert np.all(np.isfinite(matrix)), f"Invalid values in {method} matrix"
            assert np.allclose(matrix, matrix.T), f"{method} matrix not symmetric"
        
        elapsed = time.time() - start_time
        print(f"Stress test completed in {elapsed:.2f}s")
        
        # Should complete within reasonable time even under stress
        assert elapsed < 60.0, f"Stress test too slow: {elapsed:.2f}s"