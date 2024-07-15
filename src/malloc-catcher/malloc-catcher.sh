#!/bin/sh


sudo perf probe --del '*'

sudo perf probe -x /lib/x86_64-linux-gnu/libc.so.6 'malloc size=%di:s64'

sudo perf record -e 'probe_libc:*' -aR -- sleep 120
sudo chown $USER:$USER perf.data

sudo perf probe --del '*'

