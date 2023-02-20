# disable optimization, just to make sure the dead code
# is not elliminated, furthermore we need debugging symbols
# later for perf analysis
CFLAGS  = -g -O0

nifty-fifty: nifty-fifty.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf nifty-fifty
	rm -rf *.svg core
	rm -rf *.data *.data.old

disassembly: nifty-fifty
	objdump -drwC --no-show-raw-insn --visualize-jumps=extended-color ./nifty-fifty
