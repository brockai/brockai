FROM python:3.11.6

# RUN mkdir /app

WORKDIR /var/www/streamlit

COPY ./frontend /var/www/streamlit

RUN pip install -r requirements.txt

EXPOSE 8502

CMD ["streamlit", "run", "app.py"]