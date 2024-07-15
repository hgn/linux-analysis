#!/usr/bin/env python3

import os

total_free_pages = 0
try:
    with open('/proc/buddyinfo', 'r') as f:
        for line in f:
            if line.startswith('Node'):
                parts = line.split()[4:]
                for order, count in enumerate(map(int, parts)):
                    total_free_pages += count * (2 ** order)
except FileNotFoundError:
    print("/proc/buddyinfo existiert nicht")
    exit(1)

page_size = os.sysconf('SC_PAGE_SIZE')
total_free_bytes = total_free_pages * page_size
print(total_free_bytes)

