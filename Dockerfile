FROM python:3.11.5

WORKDIR /

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# COPY ./frontend .

# CMD ["streamlit", "run", "app.py"]
