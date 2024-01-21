import requests
import boto3
s3 = boto3.resource('s3')

import streamlit as st
from helpers.config import domain_api, s3_key, s3_secret, s3_bucket, s3_region, s3_endpoint

@st.cache_data(show_spinner=True)
def create_embeddings():

  response = requests.get(f'{domain_api}/embeddings')
  
  if response.status_code == 200:
      print("Request successful!")
      print(response.json())
  else:
      print("Request failed!")
      print(response.text)

def uploadFiles(byte_data, file_name):
    s3 = boto3.client('s3',
        region_name=s3_region,
        aws_access_key_id=s3_key,
        endpoint_url=s3_endpoint,
        aws_secret_access_key=s3_secret)
    
    try:
        s3.put_object(Body=byte_data, Bucket=s3_bucket, Key=st.session_state.tenant_id+'/'+file_name, ContentType='text/csv')
        st.success('File Successfully Uploaded')
        return True
    except FileNotFoundError:
        st.error('File not found.')
        return False           