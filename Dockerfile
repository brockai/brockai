FROM python:3

# WORKDIR /usr/src/app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD [ "python", "./your-daemon-or-script.py" ]

#FROM python:3.11.5

# RUN mkdir /app

# WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/brockai/brockai.git .

# RUN pip3 install -r requirements.txt

# EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]