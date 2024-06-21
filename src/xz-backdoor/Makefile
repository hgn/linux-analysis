CC = gcc
CFLAGS = -fPIC -Wall
LDFLAGS = -shared
TARGET_LZMA = liblzma.so
TARGET_SYSTEMD = libsystemd.so
TARGET_SSHD = sshd

.PHONY: all clean run run-patched show-deps set-perf-paranoid

all: $(TARGET_LZMA) $(TARGET_SYSTEMD) $(TARGET_SSHD)

$(TARGET_LZMA): lzma.o
	$(CC) $(LDFLAGS) -o $(TARGET_LZMA) lzma.o

$(TARGET_SYSTEMD): systemd.o
	$(CC) $(LDFLAGS) -o $(TARGET_SYSTEMD) systemd.o -L. -llzma

$(TARGET_SSHD): sshd.o
	$(CC) -o $(TARGET_SSHD) sshd.o -L. -lsystemd -llzma -lssl -lcrypto -Wl,-z,now

lzma.o: lzma.c
	$(CC) $(CFLAGS) -c lzma.c

systemd.o: systemd.c
	$(CC) $(CFLAGS) -c systemd.c

sshd.o: sshd.c
	$(CC) $(CFLAGS) -Wno-deprecated-declarations -c sshd.c

clean:
	rm -f *.o $(TARGET_LZMA) $(TARGET_SYSTEMD) $(TARGET_SSHD) *.txt

set-perf-paranoid:
	sudo sysctl -w kernel.perf_event_paranoid=-1

run: all
	LD_LIBRARY_PATH=. ./$(TARGET_SSHD)

run-patched: all
	LD_AUDIT=./$(TARGET_LZMA) LD_LIBRARY_PATH=. ./$(TARGET_SSHD)

show-deps: all
	LD_LIBRARY_PATH=. lddtree ./$(TARGET_SSHD)

record: all set-perf-paranoid
	LD_LIBRARY_PATH=. perf record -e intel_pt//ub -o /tmp/perf.data -- ./$(TARGET_SSHD)
	perf script --call-trace --input /tmp/perf.data -F-time,-dso,-tid,-cpu > call-trace.txt

record-patched: all set-perf-paranoid
	LD_AUDIT=./$(TARGET_LZMA) LD_LIBRARY_PATH=. perf record -e intel_pt//ub -o /tmp/perf.data -- ./$(TARGET_SSHD)
	perf script --call-trace --input /tmp/perf.data -F-time,-dso,-tid,-cpu > call-trace-patched.txt

diff: all record record-patched

