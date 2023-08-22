FROM python:3.10

ENV PYTHONUNBUFFERED=1
RUN mkdir /proverka_api
WORKDIR /proverka_api
COPY . /proverka_api/
RUN pip install -r requirements.txt