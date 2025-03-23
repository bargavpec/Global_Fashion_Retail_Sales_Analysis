
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
6. [Visualizations](#Visualizations)
7. [Technologies Used](#technologies-used)
8. [Results](#results)

## Architecture

1. Extract : Download kaggle dataset into the local , unzip the file and extract the CSV files.
2. Load : Format the CSV files to parquet files and upload them to Google clous storage.
3. Transform : Submit spark job on dataproc cluster to load aggreagte data to Bigquery tables.
4. Visualize : Create dashboard in Looker studio pointing to Bigquery dataset.
5. Orchestration: All ELT steps are automated via Airflow DAG. We can schedule as per need.
6. Infrastructure: Google cloud storage bucket, Bigquery dataset & Dataproc cluster provisioned by Terraform.

![Architecture Diagram](https://github.com/bargavpec/Global_Fashion_Retail_Sales_Analysis/blob/main/images/Architecture%20Diagram.jpg)

## Project Structure

The project folder is organized as follows:

```
/global-fashion-retail-sales
├── /data                # Raw and cleaned data files (Note: Pls check (#data-sources) for all input files)
├── /scripts             # Python scripts for data processing and analysis
├── /dags                # Airflow dags
├── /terraform           # Terraform .tf files
├── /images              # Architecture diagram & Looker dashboard
├── README.md            # Project overview and instructions
└── requirements.txt     # List of required Python packages
```

## Installation Guide

To get started with this project, you'll need to have Python 3.8+ installed. Follow these steps to set up the environment:

1. Clone the repository:
   ```
   git clone https://github.com/bargavpec/Global_Fashion_Retail_Sales_Analysis.git
   cd Global_Fashion_Retail_Sales_Analysis
   ```

2. Install Docker and validate it by running command: docker --version
3. Install Terraform and validate it by running command: terraform --version
   https://developer.hashicorp.com/terraform/install
5. Create resources: GCS bucket, Bigquery dataset & Dataproc cluster:   
   ```
   terraform init
   terraform plan
   terraform apply
   ```
6. Docker spin up the containers using docker compose:
   ```
   docker-compose up -d
   ```
7. Run the project:
   Go to Airflow console & run the Airflow DAGs to begin your analysis. For example:
   ```
   Airflow console: http://localhost:8080/
   ```
8. Once DAG run is success, shut down the containers:
   ```
   docker-compose down
   ```
9. Destroy resources when not needed anymore: GCS bucket, Bigquery dataset & Dataproc cluster:   
   ```
   terraform destroy
   ```

## Data Sources

The primary data sources for this project include:
- Global fashion retail sales data from [Kaggle] https://www.kaggle.com/datasets/ricgomes/global-fashion-retail-stores-dataset

## Usage

### 1. Sales Data Processing
Run `dags/data_ingestion_gcs.py` in Airflow to process the sales data, which includes:
- Download Kaggle dataset
- Unzip and extract the CSV files
- Format CSV files to Parquet
- Upload parquet files to Google Cloud Storage
- Submit spark job on dataproc cluster to create aggregate table in Bigquery, spark code in `scripts/spark_ingest.py` 

### 2. Insights
- Login to Looker studio, connect to data source in Bigquery and generate a dashboard including different charts like Timeseries, bubble map etc

## Visualizations

1. Sales numbers per product category
2. Geographical view of sales numbers by country
3. Trnsaction type analysis by country
4. Total sales over the years

Looker Dashboard : https://lookerstudio.google.com/reporting/8d414e07-00ae-4cbd-81a1-63db192bdf95

![Global Fashion Retail Sales Analysis Dashboard](https://github.com/bargavpec/Global_Fashion_Retail_Sales_Analysis/blob/main/images/Global%20Retail%20Sales%20Analysis.jpg)


## Technologies Used

- **Docker**: Build & run Containers.
- **Terraform**: Iaac - build resources.
- **Apache Airflow**: Data Orchestration.
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






