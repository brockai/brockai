FROM python:3.11.5

WORKDIR /app

COPY ./frontend/requirements.txt .
RUN pip install -r requirements.txt

COPY ./frontend .

CMD ["streamlit", "run", "app.py"]
