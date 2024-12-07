#!/usr/bin/env python3

import os
import random
import subprocess
import time

FILE_LIST = [
    "/usr/share/dict/words", "/usr/share/mime/mime.cache", "/usr/share/zoneinfo/UTC",
    "/usr/share/doc/apt/changelog.Debian.gz", "/usr/share/doc/apt/copyright", 
    "/usr/share/doc/bash/README", "/usr/share/doc/coreutils/README.Debian", 
    "/usr/share/doc/grep/NEWS.gz", "/usr/share/doc/findutils/changelog.Debian.gz",
    "/usr/share/doc/sed/README.Debian", "/usr/share/man/man1/ls.1.gz", 
    "/usr/share/man/man1/cat.1.gz", "/usr/share/man/man5/fstab.5.gz", 
    "/usr/share/man/man5/passwd.5.gz", "/usr/share/man/man5/shadow.5.gz",
    "/usr/share/man/man5/group.5.gz", "/usr/share/man/man8/useradd.8.gz", 
    "/usr/share/man/man8/userdel.8.gz", "/usr/share/doc/util-linux/README.Debian",
    "/usr/share/doc/dpkg/README.Debian", "/usr/share/doc/libc6/README.Debian", 
    "/usr/share/doc/e2fsprogs/README", "/usr/share/doc/nano/README.Debian",
    "/usr/share/doc/vim-common/README.Debian", "/usr/share/doc/gnupg/README",
    "/usr/share/info/coreutils.info.gz", "/usr/share/info/grep.info.gz",
    "/usr/share/info/sed.info.gz", "/usr/share/info/tar.info.gz", 
    "/usr/share/info/make.info.gz", "/usr/share/info/nano.info.gz",
    "/usr/share/info/util-linux.info.gz", "/usr/share/info/diff.info.gz",
    "/usr/share/info/psmisc.info.gz", "/usr/share/man/man5/inittab.5.gz", 
    "/usr/share/man/man8/cron.8.gz", "/usr/share/man/man8/useradd.8.gz",
    "/usr/share/man/man8/userdel.8.gz", "/usr/share/doc/xz-utils/NEWS.gz",
    "/usr/share/doc/zlib1g/NEWS.gz", "/usr/share/doc/tar/NEWS.gz",
    "/usr/share/doc/psmisc/README", "/usr/share/doc/file/README", 
    "/usr/share/doc/util-linux/copyright", "/usr/share/doc/bash/README.Debian",
    "/usr/share/doc/diffutils/README.Debian", "/usr/share/doc/ncurses-base/README",
    "/usr/share/doc/tar/README.Debian", "/usr/share/doc/xz-utils/README", 
    "/usr/share/doc/zlib1g/README.Debian", "/usr/share/doc/gawk/README", 
    "/usr/share/doc/gzip/README", "/usr/share/doc/vim/README.Debian",
    "/usr/share/doc/tzdata/README.Debian", "/usr/share/doc/e2fsprogs/NEWS.gz",
    "/usr/share/doc/util-linux/NEWS.gz", "/usr/share/doc/grep/NEWS.gz",
    # Add more paths here up to 200 files
]

PERF_EVENTS = (
    "iomap:*,filemap:*,filelock:*,ext4:*,writeback:*,block:*,"
    "syscalls:sys_enter_openat,syscalls:sys_enter_read,syscalls:sys_enter_close,"
    "syscalls:sys_exit_openat,syscalls:sys_exit_read,syscalls:sys_exit_close,"
    "sched:sched_switch"
)

def drop_caches():
    """Drop the file system caches."""
    try:
        subprocess.run(['sudo', 'sh', '-c', 'echo 3 > /proc/sys/vm/drop_caches'], check=True)
        print("Caches dropped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error dropping caches: {e}")
        exit(1)

def select_random_file():
    """Select a random file from the list."""
    return random.choice(FILE_LIST)

def run_perf(filename, output_file):
    """Run perf with the specified file and output file."""
    try:
        subprocess.run(
            [
                'sudo', 'perf', 'record', '-o', output_file, '-e', PERF_EVENTS, 
                '--', './fs-file-reader', filename
            ],
            check=True
        )
        print(f"Perf recorded successfully to {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running perf: {e}")
        return False

def main():
    while True:
        filename = select_random_file()
        print(f"Attempting to access file: {filename}")

        drop_caches()
        time.sleep(1.0)

        if run_perf(filename, "perf-uncached.data"):
            break

    run_perf(filename, "perf-cached.data")

if __name__ == "__main__":
    main()

