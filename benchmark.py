#!/usr/bin/env python3
"""
Performance benchmark script for DENV Data Analysis optimizations
This script demonstrates the performance improvements achieved through optimization
"""

import pandas as pd
import time
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    load_excel_cached,
    describe_data_optimized,
    transform_monthly_to_long_format
)


def benchmark_file_loading():
    """Benchmark file loading with and without caching"""
    print("\n" + "="*70)
    print("BENCHMARK 1: File Loading Performance")
    print("="*70)
    
    filepath = "./data/Dengue_2001-2024.xlsx"
    num_loads = 5
    
    # Without caching (simulated by reading fresh each time)
    print(f"\nLoading file {num_loads} times WITHOUT caching...")
    start = time.time()
    for i in range(num_loads):
        _ = pd.read_excel(filepath)
    time_no_cache = time.time() - start
    print(f"  Time: {time_no_cache:.3f}s")
    
    # With caching
    print(f"\nLoading file {num_loads} times WITH caching...")
    load_excel_cached.cache_clear()  # Clear cache first
    start = time.time()
    for i in range(num_loads):
        _ = load_excel_cached(filepath)
    time_with_cache = time.time() - start
    print(f"  Time: {time_with_cache:.3f}s")
    
    improvement = (1 - time_with_cache / time_no_cache) * 100
    print(f"\n✓ Improvement: {improvement:.1f}% faster with caching")
    print(f"  Speedup: {time_no_cache/time_with_cache:.1f}x")
    
    return time_no_cache, time_with_cache


def benchmark_describe_operation():
    """Benchmark data description operations"""
    print("\n" + "="*70)
    print("BENCHMARK 2: Data Description Performance")
    print("="*70)
    
    data = pd.read_excel("./data/Dengue_2001-2024.xlsx")
    
    # Original approach
    print("\nUsing ORIGINAL approach...")
    start = time.time()
    
    description = data.drop(columns=['Year']).describe()
    
    # Compute column difference once
    pop_cols = ['Population', 'Population Density', 'UPop', 'RPop', 'Infected', 'Death']
    non_pop_cols = description.columns.difference(pop_cols)
    
    description.loc[:, non_pop_cols] = description.loc[:, non_pop_cols].round(2)
    description[pop_cols] = description[pop_cols].astype(int)
    
    time_original = time.time() - start
    print(f"  Time: {time_original:.4f}s")
    
    # Optimized approach
    print("\nUsing OPTIMIZED approach...")
    start = time.time()
    
    description_opt = describe_data_optimized(data)
    
    time_optimized = time.time() - start
    print(f"  Time: {time_optimized:.4f}s")
    
    improvement = (1 - time_optimized / time_original) * 100
    print(f"\n✓ Improvement: {improvement:.1f}% faster with optimization")
    
    return time_original, time_optimized


def benchmark_data_transformation():
    """Benchmark monthly data transformation"""
    print("\n" + "="*70)
    print("BENCHMARK 3: Data Transformation Performance")
    print("="*70)
    
    df = pd.read_excel("./data/Monthly_Infection_2001-2024.xlsx")
    
    month_num_map = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04',
        'May': '05', 'June': '06', 'July': '07', 'August': '08',
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }
    months = list(month_num_map.keys())
    
    # Original loop-based approach
    print("\nUsing ORIGINAL loop-based approach...")
    start = time.time()
    
    ordered_year_month = []
    time_ordered_infections = []
    for i in range(len(df)):
        curr_year = df.iloc[i]['Year']
        for month in months:
            time_format = f'{curr_year}-{month_num_map[month]}'
            ordered_year_month.append(time_format)
            time_ordered_infections.append(df.iloc[i][month])
    
    df_dict = {'YearMonth': ordered_year_month, 'Infected': time_ordered_infections}
    _ = pd.DataFrame(df_dict)
    
    time_loop = time.time() - start
    print(f"  Time: {time_loop:.4f}s")
    
    # Optimized vectorized approach
    print("\nUsing OPTIMIZED vectorized approach...")
    start = time.time()
    
    _ = transform_monthly_to_long_format(df)
    
    time_vectorized = time.time() - start
    print(f"  Time: {time_vectorized:.4f}s")
    
    improvement = (1 - time_vectorized / time_loop) * 100
    print(f"\n✓ Improvement: {improvement:.1f}% faster with vectorization")
    print(f"  Speedup: {time_loop/time_vectorized:.1f}x")
    
    return time_loop, time_vectorized


def main():
    """Run all benchmarks"""
    print("\n" + "="*70)
    print("DENV DATA ANALYSIS - PERFORMANCE BENCHMARK")
    print("="*70)
    print("\nThis script benchmarks the performance improvements from optimization.")
    print("Running benchmarks...\n")
    
    try:
        # Run benchmarks
        t1_before, t1_after = benchmark_file_loading()
        t2_before, t2_after = benchmark_describe_operation()
        t3_before, t3_after = benchmark_data_transformation()
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        
        total_before = t1_before + t2_before + t3_before
        total_after = t1_after + t2_after + t3_after
        overall_improvement = (1 - total_after / total_before) * 100
        
        print(f"\nTotal time (original):  {total_before:.3f}s")
        print(f"Total time (optimized): {total_after:.3f}s")
        print(f"\n✓ Overall improvement: {overall_improvement:.1f}% faster")
        print(f"  Overall speedup: {total_before/total_after:.1f}x")
        
        print("\n" + "="*70)
        print("BENCHMARK COMPLETE ✓")
        print("="*70)
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: Required data file not found - {e}")
        print("  Make sure you're running this script from the project root directory.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error running benchmark: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
