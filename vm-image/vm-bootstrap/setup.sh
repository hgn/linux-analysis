#!/bin/bash

BASEPATH=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

cp ${BASEPATH}/sources.list /etc/apt/sources.list
cp ${BASEPATH}/99-perf.conf /etc/sysctl.d/99-perf.conf
apt-get --yes update
apt-get --yes upgrade
# remove some unrequired files, debug package requires some free mem
rm -rf /var/cache/apt/archives/*
apt-get --yes install linux-image-amd64-dbg sudo
apt-get --yes install aptitude mcedit build-essential vim-nox nano zsh bash screen tmux
apt-get --yes install llvm-11-dev llvm-11-tools lsof gdb cscope
apt-get --yes install perf-tools-unstable linux-perf strace ltrace trace-cmd
apt-get --yes install binutils-bpf bpfcc-tools bpftool bpftrace libbpf-dev
# for building perf
apt-get --yes install bison flex libdw-dev systemtap-sdt-dev libunwind-dev
apt-get --yes install libssl-dev libslang2-dev python3-dev binutils-dev libcap-dev
# do it now, after installation, to overwrite it in any case
cp ${BASEPATH}/sudoers /etc/sudoers

rm -rf /var/cache/apt/archives/*

# we are root, now do with do unpriv operations
su -c " \
cd /home/john; \
git clone --depth 1 https://github.com/hgn/flepa-examples.git; \
mkdir src; \
cd src; \ 
git clone --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git; \ 
git clone --depth 1 https://github.com/radareorg/radare2.git; \
" john

cp ${BASEPATH}/bashrc /home/john/.bashrc
chown john:john /home/john/.bashrc
