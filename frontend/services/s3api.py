import requests

import boto3
import streamlit as st
from helpers.config import domain_api, s3_key, s3_secret, s3_region, s3_endpoint
from st_files_connection import FilesConnection

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
        s3.put_object(Body=byte_data, Bucket=st.session_state.tenant_id, Key=file_name, ContentType='text/csv')
        st.success('File Successfully Uploaded')
        return True
    except FileNotFoundError:
        st.error('File not found.')
        return False           
    
def getFiles(): 

    #TODO: this may not be required as data will be automatically stored in opensearch after upload
    # need to add signed key, boto seems to default to aws url, this code works if directory listing left open on spaces
    # when locked returns 403 access denied
    # headers = {
    #     'Content-Type': 'application/xml',
    # }  

    response = requests.get('https://brockai.sfo3.digitaloceanspaces.com')
    # st.write(response.status_code)
    # st.write(response.text)
# 


