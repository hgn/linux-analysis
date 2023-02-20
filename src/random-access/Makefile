

CFLAGS := -g -Wall -Wextra -O2

random-access: random-access.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf random-access random-access.o
	rm -rf *.svg
	rm -rf *.data *.data.old
