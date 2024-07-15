#!/bin/sh

rm -rf gen-100-mebibytes
mkdir -p gen-100-mebibytes

echo "Generating 100 x 100 MiB files, this may take some seconds"
for i in $(seq -w 001 100); do
  dd if=/dev/urandom of=gen-100-mebibytes/$i bs=1M count=100 >/dev/null 2>&1
done

sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'

free -m
cat /proc/meminfo > meminfo-before-cat.txt

echo "Now cat 100 x 100 MiB"
cat gen-100-mebibytes/* >/dev/null
free -m
cat /proc/meminfo > meminfo-after-cat-100-mebibytes.txt


rm -rf gen-100-mebibytes
