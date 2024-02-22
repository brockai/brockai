import airflow_client.client
import streamlit as st
from airflow_client.client.api import config_api, dag_api, dag_run_api, connection_api, monitoring_api

from airflow_client.client.model.dag_run import DAGRun
from helpers.config import airflow_configuration
from services.platform_service import platform_log

monitoring_api.ApiClient()
api_client = airflow_client.client.ApiClient(airflow_configuration)
monitoring_api = monitoring_api.MonitoringApi(api_client)
connection_api = connection_api.ConnectionApi(api_client)
dag_api = dag_api.DAGApi(api_client)

verify_ssl = True

def get_connection_health(): 

    try:
        response = connection_api.get_connections()

        connection_health = f"Web 👎"
        if len(response['connections']) > 0:
            connection_health = f"Web 👍"
        
        return connection_health
    
    except airflow_client.client.OpenApiException as e:
        error_message = str(e)
        if 'tenant_id' in st.session_state:
            tenant_id = st.session_state['tenant_id']    
            platform_log('error', 'get health failed: '+error_message, 'platform_service', tenant_id)

        return e

def get_database_scheduler_health(): 

    try:
        response = monitoring_api.get_health()

        database_health = f"Database 👎"
        if response['metadatabase']['status']:
            database_health = f"Database 👍"

        scheduler_health = f"Scheduler 👎"
        if response['scheduler']['status']:
            scheduler_health = f"Scheduler 👍"

        return {'database': database_health, 'scheduler': scheduler_health}
    
    except airflow_client.client.OpenApiException as e:
        error_message = str(e)
        if 'tenant_id' in st.session_state:
            tenant_id = st.session_state['tenant_id']    
            platform_log('error', 'get health failed: '+error_message, 'platform_service', tenant_id)

        return e

def get_dag_list(): 

    try:
        response = dag_api.get_dags()
        return response
    
    except airflow_client.client.OpenApiException as e:
        error_message = str(e)
        if 'tenant_id' in st.session_state:
            tenant_id = st.session_state['tenant_id']    
            platform_log('error', 'get dag list failed: '+error_message, 'platform_service', tenant_id)

        return e

# Enter a context with an instance of the API client
# with airflow_client.client.ApiClient(airflow_configuration) as api_client:

#     errors = False

#     print('[blue]Getting DAG list')
#     dag_api_instance = dag_api.DAGApi(api_client)
#     try:
#         api_response = dag_api_instance.get_dags()
#         print(api_response)
#     except airflow_client.client.OpenApiException as e:
#         print("[red]Exception when calling DagAPI->get_dags: %s\n" % e)
#         errors = True
#     else:
#         print('[green]Getting DAG list successful')


#     print('[blue]Getting Tasks for a DAG')
#     try:
#         api_response = dag_api_instance.get_tasks(DAG_ID)
#         print(api_response)
#     except airflow_client.client.exceptions.OpenApiException as e:
#         print("[red]Exception when calling DagAPI->get_tasks: %s\n" % e)
#         errors = True
#     else:
#         print('[green]Getting Tasks successful')


#     print('[blue]Triggering a DAG run')
#     dag_run_api_instance = dag_run_api.DAGRunApi(api_client)
#     try:
#         # Create a DAGRun object (no dag_id should be specified because it is read-only property of DAGRun)
#         # dag_run id is generated randomly to allow multiple executions of the script
#         dag_run = DAGRun(
#             dag_run_id='some_test_run_' + uuid.uuid4().hex,
#         )
#         api_response = dag_run_api_instance.post_dag_run(DAG_ID, dag_run)
#         print(api_response)
#     except airflow_client.client.exceptions.OpenApiException as e:
#         print("[red]Exception when calling DAGRunAPI->post_dag_run: %s\n" % e)
#         errors = True
#     else:
#         print('[green]Posting DAG Run successful')

#     # Get current configuration. Note, this is disabled by default with most installation.
#     # You need to set `expose_config = True` in Airflow configuration in order to retrieve configuration.
#     conf_api_instance = config_api.ConfigApi(api_client)
#     try:
#         api_response = conf_api_instance.get_config()
#         print(api_response)
#     except airflow_client.client.OpenApiException as e:
#         print("[red]Exception when calling ConfigApi->get_config: %s\n" % e)
#         errors = True
#     else:
#         print('[green]Config retrieved successfully')

#     if errors:
#         print ('\n[red]There were errors while running the script - see above for details')
#     else:
#         print ('\n[green]Everything went well')