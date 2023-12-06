import os
from dotenv import load_dotenv

load_dotenv()

openaikey = os.getenv("OPENAI_KEY")
domain = os.getenv("DOMAIN")
domain_platform = os.getenv("DOMAIN_PLATFORM")
scheme = os.getenv("SCHEME")

mailgun = { 
    'options': "BROCKAI",
    'key': os.getenv("MAILGUN_API_KEY"),
    'domain': os.getenv("MAILGUN_DOMAIN"),
    'admin_email': os.getenv("ADMIN_EMAIL")
}
