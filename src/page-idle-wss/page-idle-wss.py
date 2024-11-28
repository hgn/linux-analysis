#!/usr/bin/env python3

import os
import sys
import struct
import time
from typing import List, Tuple
import mmap  # For madvise

PAGE_SHIFT = 12
PAGE_SIZE = 1 << PAGE_SHIFT  # 4096 bytes
PFNF_REUSE_LIM = 5


def vaof(pid: str, regions: List[str]) -> List[Tuple[int, int]]:
    vas = []
    with open(f"/proc/{pid}/maps", 'r') as f:
        for line in f:
            parts = line.split()
            va_range = [int("0x" + x, 0) for x in parts[0].split('-')]
            if len(parts) == 5 and "anon" in regions:
                vas.append(va_range)
            elif len(parts) == 6 and parts[5] in regions:
                vas.append(va_range)

    collapsed_vas = [vas[0]]
    for r in vas[1:]:
        if collapsed_vas[-1][1] == r[0]:
            collapsed_vas[-1][1] = r[1]
        else:
            collapsed_vas.append(r)
    return collapsed_vas


def disable_huge_pages(pid: str, regions: List[str]) -> None:
    vas = vaof(pid, regions)
    for r in vas:
        start_va = r[0]
        size = r[1] - r[0]

        try:
            with mmap.mmap(-1, size, flags=mmap.MAP_SHARED, prot=mmap.PROT_READ | mmap.PROT_WRITE, offset=start_va) as m:
                m.madvise(mmap.MADV_NOHUGEPAGE)
                print(f"Huge pages disabled for region: {hex(start_va)} - {hex(r[1])}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Failed to disable huge pages for region {hex(start_va)} - {hex(r[1])}: {e}", file=sys.stderr)
            print("Hint: echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/enabled", file=sys.stderr)


def pfnofmap(pid: str, regions: List[str]) -> List[int]:
    vas = vaof(pid, regions)
    pmap_path = f"/proc/{pid}/pagemap"
    kpflg_path = "/proc/kpageflags"
    pfns = []

    with open(pmap_path, 'rb') as pmap_file, open(kpflg_path, 'rb') as kpflg_file:
        for r in vas:
            start_va = r[0]
            end_va = r[1]
            vaddr = start_va

            while vaddr <= end_va:
                offset = vaddr >> (PAGE_SHIFT - 3)
                vaddr += PAGE_SIZE

                pmap_file.seek(offset, 0)
                entry = pmap_file.read(8)
                entry = struct.unpack("Q", entry)[0]
                pfn = entry & ((1 << 55) - 1)
                if pfn == 0:
                    continue

                kpflg_file.seek(pfn * 8, 0)
                kpflags = kpflg_file.read(8)
                kpflags = struct.unpack("Q", kpflags)[0]
                if (kpflags & (1 << 5)) == 0:
                    continue
                pfns.append(pfn)
    return pfns


def setidle(pfns: List[int]) -> None:
    bitmap_path = "/sys/kernel/mm/page_idle/bitmap"
    with open(bitmap_path, 'r+b') as f:
        for pfn in pfns:
            entry_offset = (pfn // 64) * 8
            f.seek(entry_offset, os.SEEK_SET)
            entry = struct.unpack("Q", f.read(8))[0]
            entry |= (1 << (pfn % 64))
            f.seek(entry_offset, os.SEEK_SET)
            f.write(struct.pack("Q", entry))


def getidle(pfns: List[int]) -> List[bool]:
    bitmap_path = "/sys/kernel/mm/page_idle/bitmap"
    results = []
    with open(bitmap_path, 'rb') as f:
        for pfn in pfns:
            entry_offset = (pfn // 64) * 8
            f.seek(entry_offset, os.SEEK_SET)
            entry = struct.unpack("Q", f.read(8))[0]
            results.append((entry & (1 << (pfn % 64))) != 0)
    return results


def count_working_set(bits: List[bool]) -> int:
    return bits.count(False)


def main() -> None:
    if len(sys.argv) < 2 or '--' not in sys.argv:
        print("Usage: {} -- <workload command>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    sep_index = sys.argv.index('--')
    workload_cmd = sys.argv[sep_index + 1:]

    pid = os.fork()
    if pid == 0:
        os.execvp(workload_cmd[0], workload_cmd)
    else: 
        time.sleep(5)  # Wait for the workload to start
        print(f"Monitoring workload with PID {pid}", file=sys.stderr)

        mregions = "[heap],[stack],anon"
        disable_huge_pages(str(pid), mregions.split(','))

        pfns = pfnofmap(str(pid), mregions.split(','))

        while True:
            try:
                setidle(pfns)
                time.sleep(1)
                bits = getidle(pfns)
                wspages = count_working_set(bits)
                sys.stderr.write(f"{time.time():<15.3f} {wspages:>5} pages ({wspages * PAGE_SIZE // 1024:>5} KiB)\n")
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                break


if __name__ == "__main__":
    main()

