import requests

import streamlit as st
from helpers.config import domain_api, scheme

@st.cache_data(show_spinner=True)
def create_embeddings():

  response = requests.get(f'{domain_api}/embeddings')
  
  if response.status_code == 200:
      print("Request successful!")
      print(response.json())
  else:
      print("Request failed!")
      print(response.text)

def upload():

  response = requests.post(f'{domain_api}/upload')
  
  if response.status_code == 200:
      print("Request successful!")
      print(response.json())
  else:
      print("Request failed!")
      print(response.text)