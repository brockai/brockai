FROM python:3.11.5

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py"]
