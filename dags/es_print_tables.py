from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.elasticsearch.hooks.elasticsearch import ElasticsearchHook


@task(task_id='es_print_tables')
def show_tables():
    """
    show_tables queries elasticsearch to list available tables
    """
    es = ElasticsearchHook(elasticsearch_conn_id='opensearch')

    # Handle ES conn with context manager
    with es.get_conn() as es_conn:
        tables = es_conn.execute('SHOW TABLES')
        for table, *_ in tables:
            print(f"table: {table}")
    return True


# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG(
    'elasticsearch_dag',
    start_date=datetime(2021, 8, 30),
    max_active_runs=1,
    schedule_interval=timedelta(days=1),
    default_args={'retries': 1},  # Default setting applied to all tasks
    catchup=False,
) as dag:

    show_tables()