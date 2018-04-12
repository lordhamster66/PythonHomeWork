#!/usr/bin/env bash
session_tag=$1
strace_log_path=$2
#echo "--- $session_tag ---"
#echo "--- $strace_log_path ---"
for i in $(seq 1 30);
do
    process_id=$(ps -ef |grep $session_tag |grep -v sshpass|grep -v grep |grep -v $0 |awk '{ print $2 }')
    #echo "--- process id: $process_id ---"
    if [ ! -z $process_id ];then
        #echo 'running str4ack'
        sudo strace -ttt -p $process_id -o  $strace_log_path
        break;
    fi;
    sleep 1;
done;
