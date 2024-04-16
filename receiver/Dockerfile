FROM python:3.10
USER root

RUN apt update && apt -y install vim && apt -y install cron && apt -y install net-tools && apt -y install procps && apt install -y dumb-init && apt install -y clickhouse-client && apt install -y curl && apt install -y ntp && apt clean

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/timezone && echo 'Asia/Seoul' > /etc/timezone
RUN mkdir -p /data/waf/syslog_files


COPY requirements.txt .
COPY insert.sh /home/syslog_db_insert.sh
COPY syslog_logging.py /home/
RUN chmod +x /home/syslog_db_insert.sh

RUN pip3 install -r requirements.txt