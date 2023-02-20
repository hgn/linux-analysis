

CFLAGS := -g
CFLAGS_FAST := -DNO_DEBUG -O6 -malign-double -funroll-all-loops

clean:
	rm -rf random-branch random-branch.o
	rm -rf *.svg
	rm -rf *.data *.data.old

random-branch: random-branch.c
	$(CC) $(CFLAGS) $< -o $@
