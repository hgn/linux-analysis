CFLAGS := -g -W -Wextra

ying-yang: ying-yang.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf ying-yang ying-yang.o
	rm -rf *.svg
	rm -rf *.data *.data.old

run: ying-yang
	sudo ~/bin/perf timechart record taskset -c 7 ./ying-yang
	sudo ~/bin/perf timechart
