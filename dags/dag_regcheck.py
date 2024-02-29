from airflow import DAG
from airflow.providers.elasticsearch.operators.elasticsearch import ElasticsearchOperator
from datetime import datetime, timedelta

# Replace with your OpenSearch endpoint and query
endpoint = "http://airflow.brockai.com:8080/api/v1"
index = "platform_bclayton403_files"  
query = {
  "size": 10,
  "query": {
    "match_all": {}
  }
}

# Define the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 2, 29),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="dag_regcheck",
    default_args=default_args,
    schedule_interval=None,
)

# Define the task to connect to OpenSearch and run the query
run_query_task = ElasticsearchOperator(
    task_id="run_query",
    elasticsearch_conn_id="opensearch",
    index=index,
    body=query,
    dag=dag,
)

# Define the task flow
run_query_task
