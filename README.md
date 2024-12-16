# Dengue Virus Data Analysis in Bangladesh

This project involves analyzing a dataset of Dengue virus cases in Bangladesh, spanning multiple years. The dataset includes information on monthly case counts, demographics, environmental factors, and outcomes, such as infections and deaths.

## Project Objectives

1. **Understand Temporal Trends**
   - Analyze yearly and monthly trends in Dengue cases.
   - Identify seasonal patterns in Dengue outbreaks.

2. **Explore Demographic Correlations**
   - Examine the relationship between urban and rural populations and Dengue case distribution.

3. **Investigate Environmental Impacts**
   - Study the effects of weather variables (e.g., temperature, rainfall, humidity) on Dengue case occurrences.

4. **Assess Disease Severity**
   - Calculate the case fatality rate (deaths per infected cases) and observe trends over time.

## Dataset Overview

The dataset contains the following key columns:

- **Year**: Reporting year.
- **Monthly Case Data**: Dengue cases reported for each month (January to December).
- **UrbanPop & RuralPop**: Urban and rural population counts.
- **Weather Data**:
  - Maximum temperature (Max T)
  - Minimum temperature (Min T)
  - Rainfall
  - Precipitation
  - Humidity
  - Dry-bulb temperature
- **Outcomes**:
  - Total infected cases (`Infected`)
  - Deaths (`Death`)

## Analysis Plan

### 1. Temporal Analysis
- Visualize yearly and monthly trends.
- Use line plots and heatmaps to identify seasonal patterns.

### 2. Demographic Correlation
- Compare urban vs. rural populations and their correlation with Dengue case counts.

### 3. Environmental Impact
- Perform correlation analysis to explore relationships between weather variables and Dengue cases.
- Use regression models to identify significant predictors of outbreaks.

### 4. Severity Assessment
- Calculate yearly case fatality rates.
- Visualize trends in mortality and severity over time.

## Tools and Technologies

- **Python**: Primary language for data analysis.
  - Libraries: `pandas`, `matplotlib`, `seaborn`, `scikit-learn`
- **Jupyter Notebooks**: For exploratory data analysis and visualization.
- **GitHub**: Version control and project collaboration.

## File Structure

```
├── data/
│   └── DENV_data.xlsx       # Dataset file
├── main.ipynb               # Data analysis
├── images/                  # Saved plots and figures
└── README.md                # Project description
```

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone <[repository_url](https://github.com/awnonbhowmik/DENV-Data-Analysis)>
   cd <DENV-Data-Analysis>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Jupyter Notebooks for specific analyses:
   ```bash
   jupyter notebook
   ```

## Results

The project aims to produce:
- Yearly and seasonal trend visualizations.
- Correlation analysis reports between demographics, weather, and Dengue cases.
- Regression models predicting Dengue outbreaks based on environmental variables.
- Use machine learning models for more robust predictions.

&copy; 2024 All Rights Reserved
