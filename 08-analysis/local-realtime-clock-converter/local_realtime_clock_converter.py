#!/usr/bin/env python3

import sys
import time
import datetime


# calculate delta, CLOCK_MONOTONIC_RAW reflect kernels local time (sched_time).
# CLOCK_MONOTONIC frequency adjustments will differ from sched_time
reftime = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
realtime = time.clock_gettime(time.CLOCK_REALTIME)
diff = realtime - reftime

for arg in sys.argv[1:]:
    utctime = datetime.datetime.fromtimestamp((float(arg) + diff))
    utctime_fmt = utctime.isoformat('T', 'microseconds')
    print(f"{arg} -> {utctime}")
