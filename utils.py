"""
Utility functions for DENV Data Analysis
Optimized for performance with caching and vectorized operations
"""

import pandas as pd
import geopandas as gpd
from functools import lru_cache
from typing import List, Optional
import warnings

warnings.filterwarnings("ignore")


# Cache for data loading to avoid repeated file I/O
@lru_cache(maxsize=10)
def _load_excel(filepath: str) -> pd.DataFrame:
    """Internal cached loader — do not use directly (returns a shared reference)."""
    return pd.read_excel(filepath)


def load_excel_cached(filepath: str) -> pd.DataFrame:
    """
    Load Excel file with caching to avoid repeated I/O operations.
    
    Returns a copy of the cached DataFrame so that callers can freely
    modify it without corrupting the cache for subsequent calls.
    
    Call ``load_excel_cached.cache_clear()`` to invalidate the cache
    (e.g. after the underlying file has been updated on disk).
    
    Args:
        filepath: Path to the Excel file
        
    Returns:
        DataFrame with the loaded data
    """
    return _load_excel(filepath).copy()


@lru_cache(maxsize=5)
def _load_geojson(filepath: str) -> gpd.GeoDataFrame:
    """Internal cached loader — do not use directly (returns a shared reference)."""
    return gpd.read_file(filepath)


def load_geojson_cached(filepath: str) -> gpd.GeoDataFrame:
    """
    Load GeoJSON file with caching to avoid repeated I/O operations.
    
    Returns a copy of the cached GeoDataFrame so that callers can freely
    modify it without corrupting the cache for subsequent calls.
    
    Call ``load_geojson_cached.cache_clear()`` to invalidate the cache
    (e.g. after the underlying file has been updated on disk).
    
    Args:
        filepath: Path to the GeoJSON file
        
    Returns:
        GeoDataFrame with the loaded geodata
    """
    return _load_geojson(filepath).copy()


# Expose cache_clear on the public functions for backward compatibility
load_excel_cached.cache_clear = _load_excel.cache_clear
load_geojson_cached.cache_clear = _load_geojson.cache_clear


def describe_data_optimized(data: pd.DataFrame, 
                           population_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Optimized data description function.
    
    Args:
        data: DataFrame to describe
        population_cols: List of population column names to format as integers
        
    Returns:
        Described DataFrame with proper formatting
    """
    if population_cols is None:
        population_cols = ['Population', 'Population Density', 'UPop', 'RPop', 'Infected', 'Death']
    
    # Remove 'Year' if it exists
    if 'Year' in data.columns:
        data = data.drop(columns=['Year'])
    
    description = data.describe()
    
    # Separate columns into population and non-population
    available_pop_cols = [col for col in population_cols if col in description.columns]
    non_pop_cols = [col for col in description.columns if col not in available_pop_cols]
    
    # Round non-population columns more efficiently
    if non_pop_cols:
        description[non_pop_cols] = description[non_pop_cols].round(2)
    
    # Convert population columns to integers
    if available_pop_cols:
        description[available_pop_cols] = description[available_pop_cols].astype(int)
    
    return description


def transform_monthly_to_long_format(data: pd.DataFrame) -> pd.DataFrame:
    """
    Efficiently transform monthly data to long format using pandas melt.
    This replaces inefficient loop-based transformations.
    
    Args:
        data: DataFrame with Year and monthly columns
        
    Returns:
        DataFrame in long format with YearMonth and value columns
    """
    # Month names in order
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    
    # Use melt to reshape data efficiently
    data_long = data.melt(
        id_vars=['Year'],
        value_vars=months,
        var_name='Month',
        value_name='Value'
    )
    
    # Map month names to numbers
    month_num_map = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04',
        'May': '05', 'June': '06', 'July': '07', 'August': '08',
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }
    
    # Create YearMonth string efficiently
    data_long['YearMonth'] = (
        data_long['Year'].astype(str) + '-' + 
        data_long['Month'].map(month_num_map)
    )
    
    # Select and sort
    result = data_long[['YearMonth', 'Value']].sort_values('YearMonth').reset_index(drop=True)
    
    return result


def normalize_data_efficient(data: pd.DataFrame, 
                            feature_cols: List[str],
                            target_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Efficiently normalize data using vectorized operations.
    
    Args:
        data: DataFrame to normalize
        feature_cols: List of feature columns to normalize
        target_cols: Optional list of target columns to add back without normalization
        
    Returns:
        Normalized DataFrame
    """
    # Select and convert to numeric in one step
    normalized_data = data[feature_cols].apply(pd.to_numeric)
    
    # Standardize using vectorized operations
    normalized_data = (normalized_data - normalized_data.mean()) / normalized_data.std()
    
    # Clip extreme values
    normalized_data = normalized_data.clip(lower=-3, upper=3)
    
    # Add target columns back if specified
    if target_cols:
        for col in target_cols:
            if col in data.columns:
                normalized_data[col] = data[col]
    
    return normalized_data


def add_compass_arrows(ax, arrow_base_x=0.9, arrow_base_y=0.9, arrow_length=0.05):
    """
    Add compass arrows to a matplotlib axis.
    Optimized to reduce code duplication.
    
    Args:
        ax: Matplotlib axis object
        arrow_base_x: X position of arrow base in axes coordinates
        arrow_base_y: Y position of arrow base in axes coordinates
        arrow_length: Length of arrows in axes coordinates
    """
    from matplotlib.patches import FancyArrow
    
    # Define arrows: (dx, dy, label, label_offset_x, label_offset_y)
    arrows = [
        (0, arrow_length, 'N', 0, arrow_length + 0.005),
        (0, -arrow_length, 'S', 0, -arrow_length - 0.02),
        (arrow_length, 0, 'E', arrow_length + 0.005, 0),
        (-arrow_length, 0, 'W', -arrow_length - 0.04, 0)
    ]
    
    for dx, dy, label, label_x, label_y in arrows:
        ax.add_patch(FancyArrow(
            arrow_base_x, arrow_base_y, dx, dy,
            color='black', width=0.01, length_includes_head=True,
            transform=ax.transAxes
        ))
        
        # Set text alignment based on direction
        if label in ['E', 'W']:
            text_kwargs = {'va': 'center', 'fontsize': 12, 'transform': ax.transAxes, 'weight': 'bold'}
        else:
            text_kwargs = {'ha': 'center', 'fontsize': 12, 'transform': ax.transAxes, 'weight': 'bold'}
        
        ax.text(arrow_base_x + label_x, arrow_base_y + label_y, label, **text_kwargs)


def add_scale_bar(ax, num_segments=4, scale_bar_x=0.1, scale_bar_y=0.05, 
                 scale_bar_length=0.5, scale_bar_height=0.01, max_km=200):
    """
    Add a scale bar to a matplotlib axis.
    Optimized to reduce code duplication.
    
    Args:
        ax: Matplotlib axis object
        num_segments: Number of segments in scale bar
        scale_bar_x: Starting x position in axes coordinates
        scale_bar_y: Starting y position in axes coordinates
        scale_bar_length: Total length of scale bar
        scale_bar_height: Height of scale bar
        max_km: Maximum distance in kilometers
    """
    import matplotlib.pyplot as plt
    
    segment_length = scale_bar_length / num_segments
    
    # Create segments
    for i in range(num_segments):
        ax.add_patch(plt.Rectangle(
            (scale_bar_x + i * segment_length, scale_bar_y),
            segment_length, scale_bar_height,
            color='black' if i % 2 == 0 else 'lightgray',
            transform=ax.transAxes,
            edgecolor='black',
            linewidth=1.5
        ))
    
    # Add labels
    km_step = max_km // num_segments
    for i in range(num_segments + 1):
        ax.text(
            scale_bar_x + i * segment_length, scale_bar_y - 0.01,
            f'{i * km_step} km',
            ha='center', va='top', fontsize=10, transform=ax.transAxes
        )


def annotate_map_centroids(gdf, ax, name_column='ADM1_EN'):
    """
    Annotate map with region names at centroids.
    Uses iteration for compatibility with matplotlib annotations.
    
    Args:
        gdf: GeoDataFrame with geometries
        ax: Matplotlib axis object
        name_column: Column name containing region names
    """
    # Get centroids efficiently
    centroids = gdf.geometry.centroid
    
    for idx, (name, centroid) in enumerate(zip(gdf[name_column], centroids)):
        ax.annotate(
            text=name,
            xy=(centroid.x, centroid.y),
            ha='center',
            fontweight='bold',
            color='black'
        )


def create_time_series_dataset(data, time_step=60):
    """
    Create time series dataset for LSTM efficiently using numpy.
    
    Args:
        data: Input data array
        time_step: Number of previous time steps to consider
        
    Returns:
        X, y arrays for training
    """
    import numpy as np
    
    # Pre-allocate arrays for efficiency
    n_samples = len(data) - time_step - 1
    if n_samples <= 0:
        raise ValueError(
            f"time_step ({time_step}) must be less than len(data) - 1 "
            f"({len(data) - 1}), got n_samples={n_samples}"
        )
    X = np.zeros((n_samples, time_step, 1))
    y = np.zeros(n_samples)
    
    for i in range(n_samples):
        X[i] = data[i:(i + time_step)]
        y[i] = data[i + time_step, 0]
    
    return X, y
