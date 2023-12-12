import requests
import streamlit as st
from helpers.config import domain_platform, scheme

@st.cache_data(show_spinner=True)
def create_index(index, df):
  url = scheme+domain_platform+"/"+index+"/_doc" 
  data = df.to_json(orient='records')
  print(url)
  response = requests.post(url, json=data)

  # Checking the response
  if response.status_code == 200:
      print("POST request successful!")
      print(response.json())  # Prints the response content (if any)
  else:
      print("POST request failed!")
      print(response.text)  # Prints the error message (if any)
