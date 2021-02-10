#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

cp sudoers /etc/sudoers
cp sources.list /etc/apt/sources.list
apt-get --yes update
apt-get --yes upgrade
apt-get --yes install aptitude mcedit build-essential vim-nox nano zsh bash
apt-get --yes llvm-11-dev llvm-11-tools lsof gdb
apt-get --yes install perf-tools-unstable linux-perf strace ltrace 
apt-get --yes install binutils-bpf bpfcc-tools bpftool bpftrace libbpf-dev linux-image-amd64-dbg

# we are root, now do with do unpriv operations
su -c " \
cd /home/john; \
mkdir src; \
cd src; \ 
git clone https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git; \ 
git clone https://github.com/hgn/flepa-examples.git; \
" john
