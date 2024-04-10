#!/bin/bash

CLICKHOUSE_INSERT() {
    while :; do
        for f in $(find /data/dti_waf/syslog_files -name 'syslog*'); do
            cat $f | clickhouse-client --host 211.115.206.6 --port 9001 --query="insert into default.dti_test_wafd FORMAT JSONEachRow" && rm $f
            exitcode="${?}"
            if [ $exitcode -eq 0 ]; then
                echo "$(date +%Y)/$(date +%m)/$(date +%d)-$(date +%H):$(date +%M):$(date +%S) insert into default.dti_wafd:$f"
            elif [ $exitcode -eq 210 ]; then
                echo "[INSERT ERROR]  $f Code: 210. DB::NetException: Connection refused: (172.19.191.83:9001)"
            elif [ $exitcode -eq 60 ]; then
                echo "[INSERT ERROR]  $f Code: 60. DB::Exception: Table default.dti_wafd doesn't exist.."
            elif [ $exitcode -eq 117 ]; then
                echo "[INSERT ERROR]  $f Code: 117. DB::Exception: Unknown field found while parsing JSONEachRow format"
            else
                echo "[INSERT ERROR]  $f other error.."
            fi
        done
    done
}

CLICKHOUSE_INSERT &
CLICKHOUSE_INSERT_PID=$!

echo "kill -9" $CLICKHOUSE_INSERT_PID >stop.sh

while :; do
    sleep 60
done
