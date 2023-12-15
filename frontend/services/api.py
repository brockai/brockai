import requests

import streamlit as st
from helpers.config import domain_api, scheme

@st.cache_data(show_spinner=True)
def create_embeddings():

  response = requests.get(f'{scheme}{domain_api}/embeddings')
  
  # Checking the response
  if response.status_code == 200:
      print("Request successful!")
      print(response.json())  # Prints the response content (if any)
  else:
      print("Request failed!")
      print(response.text)  # Prints the error message (if any)
