#!/usr/bin/bash

FIFO_PREFIX="perf-ctrl"
 
rm -rf ${FIFO_PREFIX}.*
 
mkfifo ${FIFO_PREFIX}.ctl
mkfifo ${FIFO_PREFIX}.ack
 
exec {perf_ctl_fd}<>${FIFO_PREFIX}.ctl
exec {perf_ack_fd}<>${FIFO_PREFIX}.ack
 
export PERF_CTL_FD=${perf_ctl_fd}
export PERF_ACK_FD=${perf_ack_fd}
 
perf stat \
    --event=task-clock,instructions \
    --delay=-1 \
    --control fd:${perf_ctl_fd},${perf_ack_fd} \
    -- ./perf-control-fifo
