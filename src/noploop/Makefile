CFLAGS := -g -O0
CFLAGS_FAST := -DNO_DEBUG -O6 -malign-double -funroll-all-loops

all: noploop

clean:
	rm -rf noploop noploop.o
	rm -rf *.svg
	rm -rf *.data *.data.old

noploop: noploop.c
	$(CC) $(CFLAGS) $< -o $@
