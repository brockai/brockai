import os
from dotenv import load_dotenv

load_dotenv()

openaikey = os.getenv("OPENAI_KEY")
domain = os.getenv("DOMAIN")
domain_api = os.getenv("DOMAIN_API")
openseearch_api = os.getenv("OPENSEARCH_API")
opensearch_platform = os.getenv("OPENSEARCH_PLATFORM")
scheme = os.getenv("SCHEME")

mailgun = { 
    'options': "BROCKAI",
    'key': os.getenv("MAILGUN_API_KEY"),
    'domain': os.getenv("MAILGUN_DOMAIN"),
    'admin_email': os.getenv("ADMIN_EMAIL")
}
