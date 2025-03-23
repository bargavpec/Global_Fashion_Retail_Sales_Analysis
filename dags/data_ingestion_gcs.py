import os

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

dataset_file = "global-fashion-retail-stores-dataset.zip"
#dataset_dir = dataset_file.replace('.zip', '')
dataset_url = "https://www.kaggle.com/api/v1/datasets/download/ricgomes/global-fashion-retail-stores-dataset"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
parquet_file = dataset_file.replace('.csv', '.parquet')
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'Fashion_retail_sales')

PYSPARK_JOB = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": "zoomcamp"},
    "pyspark_job": {"main_python_file_uri": f"gs://{BUCKET}/code/spark_ingest.py",
                    "args":[
                        f"--input_transactions=gs://{BUCKET}/raw/transactions.parquet",
                        f"--input_products=gs://{BUCKET}/raw/products.parquet",
                        f"--input_stores=gs://{BUCKET}/raw/stores.parquet",
                        f"--output={PROJECT_ID}.{BIGQUERY_DATASET}.Product_monthly_sales",
                        f"--output_store={PROJECT_ID}.{BIGQUERY_DATASET}.Country_sales"
                            ]
                    },
    }

def format_to_parquet(src_dir):
    for file_name in os.listdir(src_dir):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(src_dir, file_name)
            table = pv.read_csv(csv_file_path)
            pq.write_table(table, csv_file_path.replace('.csv', '.parquet'))


# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, local_dir):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    for file_name in os.listdir(local_dir):
        if file_name.endswith('.parquet'):
            local_file = os.path.join(local_dir, file_name)
            object_name = f"raw/{file_name}"
            blob = bucket.blob(object_name)
            blob.upload_from_filename(local_file)


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,    
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@once",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sSL -o {path_to_local_home}/{dataset_file} {dataset_url}"
    )

    unzip_dataset_task = BashOperator(
        task_id="unzip_dataset_task",
        bash_command=f"unzip -o {path_to_local_home}/{dataset_file} -d {path_to_local_home}"
    )

    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet_task",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_dir": f"{path_to_local_home}",
        },
    )

    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "local_dir": f"{path_to_local_home}",
        },
    )

    download_dataset_task >> unzip_dataset_task >> format_to_parquet_task >> local_to_gcs_task

    #def create_bigquery_tasks(**context):
    #    for file_name in os.listdir(f"{path_to_local_home}"):
    #        if file_name.endswith('.parquet'):
    #            table_id = file_name.replace('.parquet', '')
    #            bigquery_external_table_task = BigQueryCreateExternalTableOperator(
    #                task_id=f"bigquery_external_table_task_{table_id}",
    #                table_resource={
    #                    "tableReference": {
    #                        "projectId": PROJECT_ID,
    #                        "datasetId": BIGQUERY_DATASET,
    #                        "tableId": table_id,
    #                    },
    #                    "externalDataConfiguration": {
    #                        "sourceFormat": "PARQUET",
    #                        "sourceUris": [f"gs://{BUCKET}/raw/{file_name}"],
    #                    },
    #                },
    #            )
    #            bigquery_external_table_task.execute(context)
#
    #create_bigquery_tasks_task = PythonOperator(
    #    task_id="create_bigquery_tasks_task",
    #    python_callable=create_bigquery_tasks,
    #    provide_context=True,
    #)
#
    #local_to_gcs_task >> create_bigquery_tasks_task

    submit_dataproc_job = DataprocSubmitJobOperator(
            task_id="pyspark_task", job=PYSPARK_JOB, region="us-central1", project_id=PROJECT_ID
            )
    
    local_to_gcs_task >> submit_dataproc_job
