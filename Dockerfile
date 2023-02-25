FROM python:3.8-slim-buster
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client net-tools telnet curl libpq-dev python-dev build-essential\
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
WORKDIR /trader_repo
COPY ./requirements.txt  requirements.txt
RUN pip install -r ./requirements.txt
COPY . . 
EXPOSE 5002/TCP
CMD ["python3","app.py"]

