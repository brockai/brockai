import airflow_client.client
import streamlit as st

import uuid
from datetime import datetime

from airflow_client.client.api import config_api, dag_api, dag_run_api, connection_api, monitoring_api
from airflow_client.client.model.dag_run import DAGRun

from helpers.config import airflow_configuration
from services.platform_service import platform_log

# configuration = airflow_client.client.Configuration(airflow_configuration)
api_client = airflow_client.client.ApiClient(airflow_configuration)
monitoring_client = monitoring_api.MonitoringApi(api_client)
connection_client = connection_api.ConnectionApi(api_client)

# api_client = airflow_client.client.ApiClient(configuration)
dag_api_instance = dag_api.DAGApi(api_client)
dag_run_api_instance = dag_run_api.DAGRunApi(api_client)

def get_connection_health(): 

    try:
        response = connection_client.get_connections()

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
        response = monitoring_client.get_health()

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
        response = dag_api_instance.get_dags()
        return response
    
    except airflow_client.client.OpenApiException as e:
        error_message = str(e)
        if 'tenant_id' in st.session_state:
            tenant_id = st.session_state['tenant_id']    
            platform_log('error', 'get dag list failed: '+error_message, 'platform_service', tenant_id)

        return e

def run_dag(dag_id): 

    dag_id = 'example_branch_labels'

    try:
        # Create a DAGRun object (no dag_id should be specified because it is read-only property of DAGRun)
        # dag_run id is generated randomly to allow multiple executions of the script
        dag_run = DAGRun(
            dag_run_id='some_test_run_' + uuid.uuid4().hex,
        )
        api_response = dag_run_api_instance.post_dag_run(dag_id, dag_run)
        print(api_response)
    
    except airflow_client.client.OpenApiException as e:
        error_message = str(e)
        if 'tenant_id' in st.session_state:
            tenant_id = st.session_state['tenant_id']    
            platform_log('error', 'get dag list failed: '+error_message, 'platform_service', tenant_id)

        return e
