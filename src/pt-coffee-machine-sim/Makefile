CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -g3

TARGET = coffee-machine-sim
SRC = coffee-machine-sim.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

disass: $(TARGET)
	objdump -j .text -D --visualize-jumps=color --disassembler-color=extended-color $(TARGET)

pt-record: $(TARGET)
	sudo perf record -e intel_pt/cyc,cyc_thresh=5/u ./$(TARGET)

pt-record-filtered-main: $(TARGET)
	perf record -e intel_pt/cyc,cyc_thresh=5/u --filter 'filter main @ coffee-machine-sim' ./$(TARGET)

pt-record-started-main: $(TARGET)
	perf record -e intel_pt/cyc,cyc_thresh=5/u --filter 'start main @ coffee-machine-sim' ./$(TARGET)
	# or if there a no symbols (no debug information), both possible
	# 1) objdump -d ./coffee-machine-sim | grep "<main>"
	# 2) r2 -AA -q -c "afl" coffee-machine-sim
	# perf record -e intel_pt/cyc,cyc_thresh=5/u --filter 'start 0x1149@coffee-machine-sim' ./$(TARGET)

pt-report:
	sudo perf script --dump-raw-trace           > report-dump-raw.txt
	sudo perf script --itrace=i0ns --ns -F insn > report-only-ins.txt
	sudo perf script --insn-trace=disasm        > report-disasm.txt
	sudo perf script --itrace=iybxwpe -F+flags

clean:
	rm -f $(TARGET)
	rm -rf *.dot
	rm -rf *.png
	rm -rf perf*data
	rm -rf perf*old
	rm -rf *.txt

