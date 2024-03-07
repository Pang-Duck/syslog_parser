#!/bin/bash
THREAD_CH1(){
    while :
    do
        for f in $(find /colddata/ctilab/dti_v1/app/storm/topology/sh_test/data/$1/ -name 'sh_test-*')
        do
            cat $f| clickhouse-client --host 172.19.191.83 --port 9001 --query="insert into default.$1d FORMAT JSONEachRow" && rm $f
            exitcode="${?}"
            if [ $exitcode -eq 0 ];then
                echo "$(date +%Y)/$(date +%m)/$(date +%d)-$(date +%H):$(date +%M):$(date +%S) insert into $1: $f"
            elif [ $exitcode -eq 210 ];then 
                echo "[INSERT ERROR] $1 $f Code: 210. DB::NetException: Connection refused: (172.19.191.83:9001)"
            elif [ $exitcode -eq 60 ];then 
                echo "[INSERT ERROR] $1 $f Code: 60. DB::Exception: Table $1d doesn't exist.."
            elif [ $exitcode -eq 117 ];then 
                echo "[INSERT ERROR] $1 $f Code: 117. DB::Exception: Unknown field found while parsing JSONEachRow format"
            else
                echo "[INSERT ERROR] $1 $f other error.."
            fi
        done
    done
}

THREAD_CH2(){
    while :
    do
        for f in $(find /colddata/ctilab/dti_v1/app/storm/topology/sh_test/data/$1/ -name 'sh_test-*')
        do
            cat $f| clickhouse-client --host 172.19.191.84 --port 9001 --query="insert into default.$1d FORMAT JSONEachRow" && rm $f
            exitcode="${?}"
            if [ $exitcode -eq 0 ];then
                echo "$(date +%Y)/$(date +%m)/$(date +%d)-$(date +%H):$(date +%M):$(date +%S) insert into $1: $f"
            elif [ $exitcode -eq 210 ];then 
                echo "[INSERT ERROR] $1 $f Code: 210. DB::NetException: Connection refused: (172.19.191.84:9001)"
            elif [ $exitcode -eq 60 ];then 
                echo "[INSERT ERROR] $1 $f Code: 60. DB::Exception: Table $1d doesn't exist.."
            elif [ $exitcode -eq 117 ];then 
                echo "[INSERT ERROR] $1 $f Code: 117. DB::Exception: Unknown field found while parsing JSONEachRow format"
            else
                echo "[INSERT ERROR] $1 $f other error.."
            fi
        done
    done
}

sleep 1

CH1=172.19.191.83
CH2=172.19.191.84

######## SPLUNK
THREAD_CH1 dti_fw&
THREAD_fw_PID=$!

THREAD_CH1 dti_block&
THREAD_block_PID=$!

THREAD_CH1 dti_waf&
THREAD_waf_PID=$!

THREAD_CH1 dti_eflog&
THREAD_eflog_PID=$!

######## QM
THREAD_CH2 dti_qm_http&
THREAD_http_PID=$!

THREAD_CH2 dti_qm_irc&
THREAD_irc_PID=$!

THREAD_CH2 dti_qm_mail&
THREAD_mail_PID=$!

THREAD_CH2 dti_qm_ssl&
THREAD_ssl_PID=$!

THREAD_CH1 dti_qm_dns&
THREAD_dns_PID=$!

THREAD_CH2 dti_qm_l7&
THREAD_l7_PID=$!

sleep 1

echo "kill -9 " $THREAD_fw_PID $THREAD_block_PID $THREAD_waf_PID $THREAD_eflog_PID $THREAD_http_PID $THREAD_irc_PID $THREAD_mail_PID $THREAD_ssl_PID $THREAD_dns_PID $THREAD_l7_PID > stop.sh

while :
do
    sleep 60
done
