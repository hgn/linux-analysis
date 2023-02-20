#!/usr/bin/python3

import sys
import re
import os
import psutil


MAPS_LINE_RE = re.compile(r"""
    (?P<addr_start>[0-9a-f]+)-(?P<addr_end>[0-9a-f]+)\s+  # Address
    (?P<perms>\S+)\s+                                     # Permissions
    (?P<offset>[0-9a-f]+)\s+                              # Map offset
    (?P<dev>\S+)\s+                                       # Device node
    (?P<inode>\d+)\s+                                     # Inode
    (\[stack\].*)\s+                                   # Pathname
""", re.VERBOSE)

for task in psutil.process_iter(attrs=['pid']):
    pid = task.pid
    name = task.name()
    with open("/proc/%d/maps" % pid) as fd:
        for line in fd:
            m = MAPS_LINE_RE.match(line)
            if not m:
                continue
            addr_start, addr_end, perms, offset, dev, inode, pathname = m.groups()
            stack_size = int(addr_end, 16) - int(addr_start, 16)
            print("{},{},{}".format(pid, name, stack_size))
            break

