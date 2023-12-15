import requests

import streamlit as st
from helpers.config import domain_api

@st.cache_data(show_spinner=True)
def create_embeddings():
  response = requests.put(f'{domain_api}')
  
  # Checking the response
  if response.status_code == 200:
      print("Request successful!")
      print(response.json())  # Prints the response content (if any)
  else:
      print("Request failed!")
      print(response.text)  # Prints the error message (if any)

@st.cache_data(show_spinner=True)
def create_index(index, df):

  username = 'admin'
  password = 'admin'

  # Define the mapping with a dense_vector field for embeddings
  mapping = {
    "mappings": {
      "properties": {
        "embedding_vector": {
          "type": "dense_vector",
          "dims": 100
        },
        "ProductId":    { "type" : "text" },
        "Score":     { "type" : "integer" },
        "Combined":    { "type" : "text" },
        "UserId":    { "type" : "text" },
        "Summary":    { "type" : "text" },
        "Text":    { "type" : "text" },
      }
    }
  }

  # Create the index with the specified mapping
  response = requests.put(f'{domain_api}/{index}', json=mapping, verify=False)
  
  data = df.to_json(orient='records')
  # print(url)
  # response = requests.post(url, auth=(username, password), verify=False, json=data)
  
  
  
  # Checking the response
  if response.status_code == 200:
      print("POST request successful!")
      print(response.json())  # Prints the response content (if any)
  else:
      print("POST request failed!")
      print(response.text)  # Prints the error message (if any)
