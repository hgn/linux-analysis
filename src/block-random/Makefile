

CFLAGS := -g
CFLAGS_FAST := -DNO_DEBUG -O6 -malign-double -funroll-all-loops

block-random: block-random.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf block-random block-random.o
	rm -rf *.svg
	rm -rf *.data *.data.old

run: block-random
	sudo ~/bin/perf timechart record taskset -c 7 ./block-random
	sudo ~/bin/perf timechart
