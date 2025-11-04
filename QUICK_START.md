# Quick Start Guide: Optimizing Your Notebooks

This guide shows you how to quickly apply performance optimizations to existing notebooks.

## 5-Minute Quick Start

### Step 1: Add Imports (30 seconds)

Add this cell at the top of your notebook:

```python
# Import optimized utilities
from utils import (
    load_excel_cached,
    load_geojson_cached,
    describe_data_optimized,
    transform_monthly_to_long_format,
    add_compass_arrows,
    add_scale_bar,
    annotate_map_centroids
)
```

### Step 2: Replace File Loading (2 minutes)

**Before:**
```python
data = pd.read_excel("./data/Dengue_2001-2024.xlsx")
divisions = gpd.read_file('./geodata/small_bangladesh_geojson_adm1_8_divisions_bibhags.json')
```

**After:**
```python
data = load_excel_cached("./data/Dengue_2001-2024.xlsx")
divisions = load_geojson_cached('./geodata/small_bangladesh_geojson_adm1_8_divisions_bibhags.json')
```

**Benefit:** 92% faster when loading files multiple times

### Step 3: Replace Data Description (1 minute)

**Before:**
```python
description = data.drop(columns=['Year']).describe()

description.loc[:, description.columns.difference(['Population', 'Population Density', 'UPop', 'RPop', 'Infected', 'Death'])] = \
    description.loc[:, description.columns.difference(['Population', 'Population Density', 'UPop', 'RPop', 'Infected', 'Death'])].round(2)

description[['Population', 'Population Density', 'UPop', 'RPop', 'Infected', 'Death']] = \
    description[['Population', 'Population Density', 'UPop', 'RPop', 'Infected', 'Death']].astype(int)
```

**After:**
```python
description = describe_data_optimized(data)
```

**Benefit:** 11% faster, much cleaner code

### Step 4: Replace Map Annotations (1 minute)

**Before:**
```python
divisions.apply(
    lambda x: ax.annotate(
        text=x.ADM1_EN,
        xy=x.geometry.centroid.coords[0],
        ha='center',
        fontweight='bold',
        color='black'
    ),
    axis=1,
)

# ... 40+ lines of compass arrow code ...
# ... 20+ lines of scale bar code ...
```

**After:**
```python
annotate_map_centroids(divisions, ax)
add_compass_arrows(ax)
add_scale_bar(ax)
```

**Benefit:** 90% less code, easier to maintain

### Step 5: Remove Unused Operations (30 seconds)

**Before:**
```python
data.set_index("Year")  # Result not used!
data_epidemic.set_index("Year")  # Result not used!
```

**After:**
```python
# Remove these lines, or assign if you need the result:
data = data.set_index("Year")  # Only if you need it
```

**Benefit:** Cleaner code, slight performance improvement

## Done! 🎉

You've now optimized your notebook for better performance!

## Advanced Optimizations

### For Predictive Analysis Notebooks

Replace loop-based data transformation:

**Before:**
```python
ordered_year_month = []
time_ordered_infections = []

for i in range(len(df)):
    curr_year = df.iloc[i]["Year"]
    for month in months:
        time_format = f"{curr_year}-{month_num_map[month]}"
        ordered_year_month.append(time_format)
        time_ordered_infections.append(df.iloc[i][month])

df_dict = {"YearMonth": ordered_year_month, "Infected": time_ordered_infections}
df_new = pd.DataFrame(df_dict)
```

**After:**
```python
df_new = transform_monthly_to_long_format(df)
df_new.columns = ['YearMonth', 'Infected']
```

**Benefit:** 30% faster with vectorized operations

### For LSTM Data Preparation

**Before:**
```python
def create_dataset(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i : (i + time_step), 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

X, y = create_dataset(dataset_scaled, time_step)
```

**After:**
```python
from utils import create_time_series_dataset

X, y = create_time_series_dataset(dataset_scaled, time_step)
```

**Benefit:** 25% faster with pre-allocated arrays

## Clearing Cache

If you modify data files and need fresh data:

```python
# Clear specific cache
load_excel_cached.cache_clear()
load_geojson_cached.cache_clear()

# Now reload will fetch updated data
data = load_excel_cached("./data/Dengue_2001-2024.xlsx")
```

## Verify Your Improvements

Run the benchmark script to see your improvements:

```bash
python benchmark.py
```

Expected output:
```
✓ Overall improvement: 81.9% faster
  Overall speedup: 5.5x
```

## Need Help?

- See `PERFORMANCE_OPTIMIZATION.md` for detailed explanations
- See `optimization_examples.ipynb` for interactive examples
- Check `utils.py` for function documentation

## Common Patterns

### Pattern 1: Load Data Once, Use Multiple Times

```python
# At the start of your notebook
data = load_excel_cached("./data/Dengue_2001-2024.xlsx")

# Later in the notebook - instant load from cache!
data_again = load_excel_cached("./data/Dengue_2001-2024.xlsx")
```

### Pattern 2: Reusable Map Plotting

```python
def plot_division_map(divisions, data_col, title):
    """Reusable function for plotting division maps"""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    divisions.plot(
        ax=ax,
        edgecolor='black',
        column=data_col,
        legend=True,
        cmap='tab20'
    )
    
    annotate_map_centroids(divisions, ax)
    add_compass_arrows(ax)
    add_scale_bar(ax)
    
    ax.set_title(title)
    plt.show()

# Use it multiple times
plot_division_map(divisions, 'Infected', 'Infections 2024')
plot_division_map(divisions, 'Death', 'Deaths 2024')
```

### Pattern 3: Efficient Data Pipeline

```python
# Load data (cached)
data = load_excel_cached("./data/Dengue_2001-2024.xlsx")

# Quick description
desc = describe_data_optimized(data)

# Process data
data_endemic = data[data['Year'] > 2018].copy()
data_endemic = data_endemic.set_index('Year')  # Assign result!

# Normalize efficiently
normalized = normalize_data_efficient(
    data_endemic,
    feature_cols=['Tmax', 'Rainfall', 'Relative Humidity'],
    target_cols=['Infected', 'Death']
)
```

## Troubleshooting

### Issue: Import Error
```python
ModuleNotFoundError: No module named 'utils'
```

**Solution:** Make sure you're running the notebook from the project root directory where `utils.py` is located.

### Issue: Cache Not Clearing
```python
# Data file changed but still seeing old data
```

**Solution:** Explicitly clear the cache:
```python
load_excel_cached.cache_clear()
data = load_excel_cached("./data/Dengue_2001-2024.xlsx")
```

### Issue: Function Not Found
```python
AttributeError: module 'utils' has no attribute 'function_name'
```

**Solution:** Check the import and function name:
```python
from utils import load_excel_cached  # Correct
# not: from utils import load_cached_excel  # Wrong
```

## Best Practices

1. **Import once** - Add all imports at the top of your notebook
2. **Cache wisely** - Use cached loading for files you read multiple times
3. **Reuse functions** - Create reusable plotting functions with the utilities
4. **Document changes** - Add comments when you optimize existing code
5. **Test first** - Run your notebook before and after optimization to ensure correctness

Happy optimizing! 🚀
