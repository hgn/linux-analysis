CFLAGS  = -g -O0 -Winline -Wno-div-by-zero

nebulous-crasher: nebulous-crasher.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf nebulous-crasher
	rm -rf *.data *.data.old
	rm -rf core
