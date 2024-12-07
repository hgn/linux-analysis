OBJ = fs-file-reader
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
	sudo perf record -o perf-uncached.data -e 'iomap:*,filemap:*,filelock:*,ext4:*,writeback:*,block:*,syscalls:sys_enter_openat,syscalls:sys_enter_read,syscalls:sys_enter_close,syscalls:sys_exit_openat,syscalls:sys_exit_read,syscalls:sys_exit_close,sched:sched_switch'  -- ./$(OBJ)
	sudo perf record -o perf-cached.data -e 'iomap:*,filemap:*,filelock:*,ext4:*,writeback:*,block:*,syscalls:sys_enter_openat,syscalls:sys_enter_read,syscalls:sys_enter_close,syscalls:sys_exit_openat,syscalls:sys_exit_read,syscalls:sys_exit_close,sched:sched_switch'  -- ./$(OBJ)
	#@sudo perf record -e 'syscalls:sys_enter_openat,syscalls:sys_enter_read,syscalls:sys_enter_close,syscalls:sys_exit_openat,syscalls:sys_exit_read,syscalls:sys_exit_close'  -- ./$(OBJ)

all: $(OBJ)
	record

.PHONY: all run clean

