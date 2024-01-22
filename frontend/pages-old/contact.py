import streamlit as st
from captcha.image import ImageCaptcha
st.set_page_config(layout="wide", page_title="brockai - Platform", page_icon="./static/brockai.png")  

import re
import random
import requests

from helpers.config import mailgun
from helpers.markdown import sidebar_links_footer, sidebar_app_header

from captcha.image import ImageCaptcha    

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(pattern, email):
        return True
    else:
        return False

def generate_captcha():
    captcha_text = "".join(random.choices(mailgun['options'], k=6))
    image = ImageCaptcha(width=400, height=100).generate(captcha_text)
    return captcha_text, image
  
with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +sidebar_app_header
        +sidebar_links_footer
        , unsafe_allow_html=True
    )

st.header(":email: Contact Us")

if 'captcha_text' not in st.session_state:
    st.session_state.captcha_text = generate_captcha()

col1, col2, col3, col4 =  st.columns([3, 0.25, 1, 0.25])

captcha_text, captcha_image = st.session_state.captcha_text

captcha_input = None

with col3:
    st.markdown('<p style="text-align: justify; font-size: 12px;">CAPTCHAs are active to prevent automated submissions. <br> Thank you for your understanding.</p>', unsafe_allow_html=True)
    captcha_placeholder = st.empty()
    captcha_placeholder.image(captcha_image, use_column_width=True)

    if st.button("Refresh", type="secondary", use_container_width=True):
        st.session_state.captcha_text = generate_captcha()
        captcha_text, captcha_image = st.session_state.captcha_text
        captcha_placeholder.image(captcha_image, use_column_width=True)

with col1:
    with st.form("contact_form", clear_on_submit=True):
        email = st.text_input("**Your email***")
        message = st.text_area("**Your message***")
        captcha_input = st.text_input("CAPTCHA*")
        st.markdown('<p style="font-size: 13px;">*Required fields</p>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Send")
        
    if submitted:
      
        valid = is_valid_email(email)
        
        if not email or not message:
            st.error("Please fill out all required fields.")
            
        elif valid:
            
            if captcha_input.upper() == captcha_text:
                  
                st.session_state.captcha_text = generate_captcha()
                captcha_text, captcha_image = st.session_state.captcha_text
                captcha_placeholder.image(captcha_image, use_column_width=True)
                  
                subject = "Note from brockai"
                body = f"Email: {email}\nMessage: {message}"
                    
                data = {
                    'from': email,
                    'to': mailgun['admin_email'],
                    'subject': subject,
                    'text': body
                }
                    
                mailgun_url = f"https://api.mailgun.net/v3/{mailgun['domain']}/messages"

                response = requests.post(
                    mailgun_url,
                    auth=('api', mailgun['key']),
                    data=data
                )

                if response.status_code == 200:
                    st.info("👍 Thanks, talk soon")
                        
                else:
                    st.error("Failed to send")
                       
            else:
                st.error("Text does not match the CAPTCHA.") 
                    
        else:
            st.error(f"Invalid email address.") 
