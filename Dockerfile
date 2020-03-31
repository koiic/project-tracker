#build
FROM python:3.7.3 as server

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
