# disable optimization, just to make sure the dead code
# is not elliminated, furthermore we need debugging symbols
# later for perf analysis
CFLAGS  = -g -O0

nasty-crash: nasty-crash.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf nasty-crash
	rm -rf *.data *.data.old
	rm -rf core
