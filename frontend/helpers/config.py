import os
from dotenv import load_dotenv

from authlib.integrations.requests_client import OAuth2Session

client_id = 'p5GXjSiQzUtHgbQoA7c3R60SFtN4HQF4'
client_secret = 'y4Bc-4YDooZI-7Mbul8EXUFxxUlqi5QjNlmidPFjWisK6WJ9t2sifoewohg1kK2o'
domain = 'brockai.us.auth0.com'

load_dotenv()

openaikey = os.getenv("OPENAI_KEY")
domain = os.getenv("DOMAIN")
domain_api = os.getenv("DOMAIN_API")
domain_platform = os.getenv("DOMAIN_PLATFORM")
auth0_domain = os.getenv("AUTH0_DOMAIN")
auth0_client_id = os.getenv("AUTH0_CLIENT_ID")
auth0_client_secret = os.getenv("AUTH0_CLIENT_SECRET")
auth0_redirect_uri = os.getenv("AUTH0_REDIRECT_URI")
opensearch_api = os.getenv("OPENSEARCH_API")
opensearch_platform = os.getenv("OPENSEARCH_PLATFORM")
scheme = os.getenv("SCHEME")

mailgun = { 
    'options': "BROCKAI",
    'key': os.getenv("MAILGUN_API_KEY"),
    'domain': os.getenv("MAILGUN_DOMAIN"),
    'admin_email': os.getenv("ADMIN_EMAIL")
}

auth = OAuth2Session(auth0_client_id, auth0_client_secret, scope='openid profile email', redirect_uri=domain_platform)
authorization_url, state = auth.create_authorization_url(f'https://{auth0_domain}/authorize')
