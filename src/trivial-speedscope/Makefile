

CFLAGS := -g -Wall -Wextra -O0

trivial-speedscope: trivial-speedscope.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf trivial-speedscope trivial-speedscope.o
	rm -rf *.svg
	rm -rf *.data *.data.old

run: trivial-speedscope
	pass
