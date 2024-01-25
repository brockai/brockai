import streamlit as st
import requests
from opensearchpy import OpenSearch

auth = ('backdoor', 'PearTree369!') #!For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts = [{'host': 'http://opensearch.brockai.com', 'port': 9243}],
    http_auth = auth,
    use_ssl = False,
    verify_certs = False
)

def opensearch_welcome():
  info = client.info()
  st.write(f"Welcome to {info['version']['distribution']} {info['version']['number']}!")

def check_opensearch_health():
    url = 'http://opensearch.brockai.com:9243/_cluster/health'
    st.write(url)
    # response = client.get(url)
    # try:
    # response = requests.get(url)
    # st.write(response.headers, response.status_code)
    #     if response.status_code == 200:
    #         health_info = response.json()
    #         print(f"Cluster status: {health_info['status']}")
    #     else:
    #         print(f"Failed to fetch cluster health. Status code: {response.status_code}")
    # except requests.RequestException as e:
    #     print(f"Error: {e}")


# def create_index(index_name):
#   st.write(client)
    # index_body = {
    #   'settings': {
    #     'index': {
    #       'number_of_shards': 4
    #     }
    #   }
    # }

    
    # response = client.indices.create(
    #   index_name, 
    #   body=index_body
    # )

    # st.write(response)












  # username = 'admin'
  # password = 'admin'

  # # Define the mapping with a dense_vector field for embeddings
  # mapping = {
  #   "mappings": {
  #     "properties": {
  #       "embedding_vector": {
  #         "type": "dense_vector",
  #         "dims": 100
  #       },
  #       "ProductId":    { "type" : "text" },
  #       "Score":     { "type" : "integer" },
  #       "Combined":    { "type" : "text" },
  #       "UserId":    { "type" : "text" },
  #       "Summary":    { "type" : "text" },
  #       "Text":    { "type" : "text" },
  #     }
  #   }
  # }

 
  # # Checking the response
  # if response.status_code == 200:
  #     print("POST request successful!")
  #     print(response.json())  # Prints the response content (if any)
  # else:
  #     print("POST request failed!")
  #     print(response.text)  # Prints the error message (if any)
