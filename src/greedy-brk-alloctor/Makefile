OBJ = greedy-brk-alloctor
CFLAGS = -g -fno-omit-frame-pointer -O0 -Wall -Wextra

OBJ_C = $(OBJ).c

$(OBJ): $(OBJ_C)
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf $(OBJ)
	rm -rf *.data *.data.old

record: $(OBJ)
	@echo "Clearing system caches..."
	@sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
	@echo "Running the program..."
	@sudo perf record -g -- taskset -c 6 ./$(OBJ)

report:
	sudo perf report --stdio

all: $(OBJ)
	record

.PHONY: all run clean bootstrap


