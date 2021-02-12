#!/bin/bash

BASEPATH=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

cp ${BASEPATH}/sudoers /etc/sudoers
cp ${BASEPATH}/sources.list /etc/apt/sources.list
apt-get --yes update
apt-get --yes upgrade
# remove some unrequired files, debug package requires some free mem
rm -rf /var/cache/apt/archives/*
apt-get --yes install linux-image-amd64-dbg
apt-get --yes install aptitude mcedit build-essential vim-nox nano zsh bash screen tmux
apt-get --yes install llvm-11-dev llvm-11-tools lsof gdb cscope
apt-get --yes install perf-tools-unstable linux-perf strace ltrace trace-cmd
apt-get --yes install binutils-bpf bpfcc-tools bpftool bpftrace libbpf-dev

# we are root, now do with do unpriv operations
su -c " \
cd /home/john; \
mkdir src; \
cd src; \ 
git clone https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git; \ 
git clone --depth 1 https://github.com/hgn/flepa-examples.git; \
" john

cp ${BASEPATH}/bashrc /home/john/.bashrc
chown john:john /home/john/.bashrc
