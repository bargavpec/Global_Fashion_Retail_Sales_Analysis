
# Global Fashion Retail Sales Analysis Project

## Overview

This project analyzes global fashion retail sales trends, focusing on key metrics such as revenue, growth patterns, regional differences, and consumer behavior. The goal is to provide insights that can help fashion brands, retailers, and analysts make data-driven decisions about inventory, marketing strategies, and expansion plans.

### Key Features:
- **Sales Data Analysis**: In-depth analysis of fashion retail sales data across different regions and time periods.
- **Analyze Staffing and Performance**: Evaluate store staffing ratios and analyze the impact of employee performance on store success.
- **Consumer Behavior Insights**: Insights into consumer purchasing habits and preferences in the fashion industry.
- **Market Segmentation**: Categorizing the global market by region, demographics, and fashion preferences.
  
## Table of Contents
1. [Architecture](#Architecture)
2. [Project Structure](#project-structure)
3. [Installation Guide](#installation-guide)
4. [Data Sources](#data-sources)
5. [Usage](#usage)
6. [Technologies Used](#technologies-used)
7. [Results](#results)

## Architecture

![Architecture Diagram](/images/Architecture Diagram.jpg)

## Project Structure

The project folder is organized as follows:

```
/global-fashion-retail-sales
├── /data                # Raw and cleaned data files
├── /notebooks           # Jupyter notebooks with analysis and visualizations
├── /scripts             # Python scripts for data processing and analysis
├── /results             # Output files like charts, graphs, and reports
├── /docs                # Documentation files
├── README.md            # Project overview and instructions
└── requirements.txt     # List of required Python packages
```

## Installation Guide

To get started with this project, you'll need to have Python 3.8+ installed. Follow these steps to set up the environment:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/global-fashion-retail-sales.git
   cd global-fashion-retail-sales
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Download the dataset and place it in the `/data` directory (see [Data Sources](#data-sources)).

5. Run the project:
   You can run the Jupyter notebooks or Python scripts to begin your analysis. For example:
   ```
   jupyter notebook
   ```

## Data Sources

The primary data sources for this project include:
- Global fashion retail sales data from [Kaggle] https://www.kaggle.com/datasets/ricgomes/global-fashion-retail-stores-dataset

## Usage

### 1. Sales Data Analysis
Run `notebooks/sales_analysis.ipynb` to analyze the sales data, including:
- Revenue analysis by region
- Year-over-year growth trends
- Product category performance

### 2. Forecasting Future Sales
The forecasting module in `scripts/forecasting.py` uses machine learning algorithms to predict sales trends for the next quarters. 

```python
from forecasting import forecast_sales

# Predict sales for the next quarter
forecast_sales(data)
```

### 3. Consumer Insights
Run `notebooks/consumer_behavior.ipynb` to generate insights on consumer preferences, focusing on demographic factors, fashion styles, and spending habits.

## Visualizations

1. Sales numbers per product category
2. Geographical view of sales numbers by country
3. Trnsaction type analysis by country
4. Total sales over the years
   Dashboard : https://lookerstudio.google.com/reporting/8d414e07-00ae-4cbd-81a1-63db192bdf95


## Technologies Used

- **Docker**: Containers.
- **Apache Airflow**: Orchestration.
- **Looker Studio**: Data visualization.
- **Google Bigquery**: Cloud Datawarehouse.
- **Google cloud storage**: Storage layer.
- **Google Dataproc**: Managed spark service.
- **Spark**: Data processing.

## Results

The analysis reveals the following key insights:
1. **Growth**: The global fashion retail market grew by X% over the past Y years, with significant growth in region A.
2. **Trends**: The most popular fashion trends in Q1 2025 include sustainable fashion and athleisure.
3. **Consumer Insights**: Consumers in region A tend to favor luxury brands, while region B shows a preference for affordable, fast fashion.
4. **Forecasting**: Based on current trends, the fashion retail industry is expected to grow by Z% in the next 12 months.

For detailed results, please check the notebooks in the `/notebooks` folder.





