#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

cp sudoers /etc/sudoers
cp source.list /etc/apt/source.list
apt-get --yes --force-yes update
apt-get --yes --force-yes upgrade

apt-get --yes --force-yes install mc-edit build-essential vim-nox nano llvm-11-dev llvm-11-tools

# we are root, now do with do unpriv operations
su john
cd $HOME
mkdir src
cd src
git clone https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
git clone https://github.com/hgn/flepa-examples.git
