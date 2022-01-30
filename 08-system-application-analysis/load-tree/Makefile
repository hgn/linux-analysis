# disable optimization, just to make sure the dead code
# is not elliminated, furthermore we need debugging symbols
# later for perf analysis
CFLAGS  = -g -O0

load-tree: load-tree.c
	$(CC) -Wa,-ahl=load-tree.s $(CFLAGS) $< -o $@

load-tree.s: load-tree.c
	$(CC) -S $(CFLAGS) $< -o $@

clean:
	rm -rf load-tree load-tree.s
	rm -rf *.svg
	rm -rf *.data *.data.old

disassembly: load-tree
	objdump -drwC --no-show-raw-insn --visualize-jumps=extended-color ./load-tree

run: load-tree
