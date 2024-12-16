CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -g3

TARGET = cms
SRC = cms.c

DOT_DIR = llvm-control-flow

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

llvm-control-flow: $(SRC)
	mkdir -p $(DOT_DIR)
	clang -Xclang -disable-O0-optnone  -emit-llvm  -S -o $(TARGET).ll $(TARGET).c
	opt $(TARGET).ll -passes=dot-cfg -cfg-dot-filename-prefix=$(TARGET) -disable-output
	opt $(TARGET).ll -passes=dot-callgraph -disable-output
	for file in *.dot; do \
					dot -Tpng -Gdpi=300 $$file -o $(DOT_DIR)/$$(basename $$file .dot).png; \
	done
	rm -f $(TARGET).*dot


disass: $(TARGET)
	objdump -j .text -D --visualize-jumps=color --disassembler-color=extended-color $(TARGET)

pt-record: $(TARGET)
	sudo perf record -e intel_pt/cyc,cyc_thresh=5/u ./$(TARGET)
	sudo chown $$USER:$$GROUP perf.data

pt-record-filtered-main: $(TARGET)
	sudo perf record -e intel_pt/cyc,cyc_thresh=5/u --filter 'filter main @ cms' ./$(TARGET)
	sudo chown $$USER:$$GROUP perf.data

pt-record-started-main: $(TARGET)
	sudo perf record -e intel_pt/cyc,cyc_thresh=5/u --filter 'start main @ cms' ./$(TARGET)
	sudo chown $$USER:$$GROUP perf.data
	# or if there a no symbols (no debug information), both possible
	# 1) objdump -d ./coffee-machine-sim | grep "<main>"
	# 2) r2 -AA -q -c "afl" coffee-machine-sim
	# perf record -e intel_pt/cyc,cyc_thresh=5/u --filter 'start 0x1149@cms' ./$(TARGET)

report:
	perf script --itrace=d; mv intel_pt.log report-decoder-debug.txt
	perf script --dump-raw-trace                > report-dump-raw.txt
	perf script --itrace=i0ns --ns -F insn      > report-only-ins.txt
	perf script --itrace=i0ns --ns -Fip,sym,dso > report-ip-sym-dso.txt
	perf script --insn-trace=disasm             > report-disasm.txt
	perf script --no-itrace --show-mmap-events  > report-mmap-events.txt
	# note, requires sampling not limited to userspace
	perf script --itrace=p | grep cbr - > report-power-events.txt
	#perf script --itrace=iybxwpe -F+flags
	#perf report -s srcline
	#perf report pt_ls --itrace=i1usge
	ls -l report-*

clean:
	rm -f $(TARGET)
	rm -rf *.dot
	rm -rf *.png
	rm -rf perf*data
	rm -rf perf*old
	rm -rf *.txt
	rm -rf *.ll
	rm -rf $(DOT_DIR)
	rm -rf core

