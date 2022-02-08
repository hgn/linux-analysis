# disable optimization, just to make sure the dead code
# is not elliminated, furthermore we need debugging symbols
# later for perf analysis
CFLAGS  = -g -O0 -Wno-div-by-zero

branching-spinner: branching-spinner.c
	$(CC) -Wa,-ahl=branching-spinner.s $(CFLAGS) $< -o $@

clean:
	rm -rf branching-spinner branching-spinner.s
	rm -rf *.svg core
	rm -rf *.data *.data.old

disassembly: branching-spinner
	objdump -drwC --no-show-raw-insn --visualize-jumps=extended-color ./branching-spinner
