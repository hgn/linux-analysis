# disable optimization, just to make sure the dead code
# is not elliminated, furthermore we need debugging symbols
# later for perf analysis
CFLAGS  = -g -O0

yin-yang: yin-yang.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf yin-yang
	rm -rf *.svg core
	rm -rf *.data *.data.old

disassembly: yin-yang
	objdump -drwC --no-show-raw-insn --visualize-jumps=extended-color ./yin-yang
