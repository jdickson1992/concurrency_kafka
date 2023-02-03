FROM --platform=linux/x86_64 python:3

WORKDIR /app

COPY /src /app

RUN pip install confluent-kafka