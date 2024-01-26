import os
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

openaikey = os.getenv("OPENAI_KEY")
domain = os.getenv("DOMAIN")
s3_key = os.getenv("S3_KEY")
s3_secret = os.getenv("S3_SECRET")
s3_region = os.getenv("S3_REGION")
s3_endpoint = os.getenv("S3_ENDPOINT")
auth0_domain = os.getenv("AUTH0_DOMAIN")
auth0_client_id = os.getenv("AUTH0_CLIENT_ID")
auth0_client_secret = os.getenv("AUTH0_CLIENT_SECRET")
auth0_client_audience = os.getenv("AUTH0_CLIENT_AUDIENCE")
auth0_redirect_uri = os.getenv("AUTH0_REDIRECT_URI")
auth0_authorization_url = f"{auth0_domain}/authorize"
opensearch_api = os.getenv("OPENSEARCH_API")
opensearch_platform = os.getenv("OPENSEARCH_PLATFORM")
opensearch_user = os.getenv("OPENSEARCH_USER")
opensearch_password = os.getenv("OPENSEARCH_PASSWORD")

scope = "openid profile email"
response_type = "code" 
token_url = auth0_domain+"/oauth/token"
userinfo_url = auth0_domain+"/userinfo"

scheme = os.getenv("SCHEME")

mailgun = { 
    'options': "BROCKAI",
    'key': os.getenv("MAILGUN_API_KEY"),
    'domain': os.getenv("MAILGUN_DOMAIN"),
    'admin_email': os.getenv("ADMIN_EMAIL")
}


domain_api = os.getenv("DOMAIN_API")
domain_platform = os.getenv("DOMAIN_PLATFORM")