import streamlit as st
import requests
from opensearchpy import OpenSearch
from helpers.config import opensearch_user, opensearch_password

# auth = (opensearch_user, opensearch_password) #!For testing only. Don't store credentials in code.

# client = OpenSearch(
#     hosts = [{'host': 'http://opensearch.brockai.com', 'port': 9243}],
#     http_auth = auth,
#     use_ssl = False,
#     verify_certs = False
# )

def check_opensearch_health():
    url = 'http://opensearch.brockai.com:9243/_cluster/health'

    try:
      response = requests.get(url, auth=(opensearch_user, opensearch_password))

      if response.status_code == 200:
          return f"Cluster Up! 👍"
      else:
          return f"Cluster Down! 👎"

    except requests.RequestException as e:
      return f"Cluster Down! 👎"
    
def create_index():
   # Replace 'your-opensearch-host' and 'your-opensearch-port' with your actual values
  opensearch_host = 'http://opensearch.brockai.com'
  opensearch_port = '9243'

  # Create an OpenSearch client
  es = OpenSearch([{'host': opensearch_host, 'port': opensearch_port}])

  # Replace 'your-index-name' with the desired index name
  index_name = st.session_state.tenant_id

  # Index settings and mappings (replace with your own settings and mappings)
  index_settings = {
      "settings": {
          "number_of_shards": 1,
          "number_of_replicas": 1
      }
  }

  index_mappings = {
      "mappings": {
          "properties": {
              "field1": {"type": "keyword"},
              "field2": {"type": "text"}
              # Add more field definitions as needed
          }
      }
  }

  try:
      # Create the index
      response = es.indices.create(index=index_name, body=index_settings, ignore=400)

      if 'acknowledged' in response and response['acknowledged']:
          print(f"Index '{index_name}' created successfully")
      else:
          print(f"Failed to create index '{index_name}'")

  except Exception as e:
      print(f"Error creating index: {e}")
