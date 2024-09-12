OBJ = call-flow-example
CFLAGS = -g -fno-omit-frame-pointer -O0 -Wall -Wextra
LIBS = $(shell pkg-config --libs libsystemd)
INCLUDES = $(shell pkg-config --cflags libsystemd)

OBJ_C = $(OBJ).c

$(OBJ): $(OBJ_C)
	$(CC) $(CFLAGS) $(INCLUDES) $< -o $@ $(LIBS)

run: $(OBJ)
	sudo perf record --call-graph dwarf -D 100 -C 10 -e 'syscalls:sys_enter_*,syscalls:sys_exit_*,sched:sched_switch,cpu_core/cycles/' -- taskset -c 10 ./call-flow-example

clean:
	rm -rf $(OBJ)
	rm -rf *.data *.data.old

all: $(OBJ) run

bootstrap:
	sudo apt install libsystemd-dev

.PHONY: all run clean bootstrap


