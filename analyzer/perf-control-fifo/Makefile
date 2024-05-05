OBJ = perf-control-fifo
CFLAGS  = -Wall -Wextra -Wpedantic -fsanitize=undefined -g -fno-omit-frame-pointer -O1

OBJ_C = $(addsuffix .c,$(OBJ))

$(OBJ): $(OBJ_C)
	$(CC) $(CFLAGS) $< -o $@ -lm

clean:
	rm -rf $(OBJ) perf_fd.ack  perf_fd.ctl 
	rm -rf *.svg core

