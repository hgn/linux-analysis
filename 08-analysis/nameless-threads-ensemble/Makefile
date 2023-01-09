CFLAGS := -g -Wall -Wextra

SRC := $(wildcard *.c)
OBJ := $(SRC:.c=)

$(OBJ): $(SRC)
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf $(OBJ)
	rm -rf *.svg
	rm -rf *.data *.data.old

run: $(OBJ)
	sudo perf sched record -- chrt --fifo 99 ./$(OBJ)
	sudo perf script report tasks-analyzer --summary

all: $(OBJ)

.PHONY: all clean run
