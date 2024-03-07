FROM python:3.10

RUN apt install vim && apt install cron && apt install net-tools && apt install procps && apt install dumb-init && apt install clickhouse-client && apt clean

COPY requirements.txt .

RUN pip3 install -r requirements.txt