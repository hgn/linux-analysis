CFLAGS  = -g -O0 -Winline -Wno-div-by-zero

nasty-crash: nasty-crash.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf nasty-crash
	rm -rf *.data *.data.old
	rm -rf core
