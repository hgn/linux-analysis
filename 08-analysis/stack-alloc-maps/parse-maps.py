#!/usr/bin/python

import sys
import re

pid = int(sys.argv[1])
stack_alloc_size = int(sys.argv[2])
counter = int(sys.argv[3])


MAPS_LINE_RE = re.compile(r"""
    (?P<addr_start>[0-9a-f]+)-(?P<addr_end>[0-9a-f]+)\s+  # Address
    (?P<perms>\S+)\s+                                     # Permissions
    (?P<offset>[0-9a-f]+)\s+                              # Map offset
    (?P<dev>\S+)\s+                                       # Device node
    (?P<inode>\d+)\s+                                     # Inode
    (\[stack\].*)\s+                                   # Pathname
""", re.VERBOSE)


with open("/proc/%d/maps" % pid) as fd:
    for line in fd:
        m = MAPS_LINE_RE.match(line)
        if not m:
            continue
        addr_start, addr_end, perms, offset, dev, inode, pathname = m.groups()
        stack_size = int(addr_end, 16) - int(addr_start, 16)
        print("{},{},{}".format(counter, stack_alloc_size, stack_size))
