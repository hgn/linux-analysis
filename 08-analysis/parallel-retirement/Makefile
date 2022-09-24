OBJ = mass-retirement
CFLAGS  = -Wall -Wextra -ggdb3 -funwind-tables -Wall -Wextra -std=gnu99 -fno-omit-frame-pointer -O2

OBJ_C = $(addsuffix .c,$(OBJ))
OBJ_S = $(addsuffix .s,$(OBJ))

$(OBJ): $(OBJ_C)
	$(CC) -Wa,-ahl=$(OBJ_S) $(CFLAGS) $< -o $@

clean:
	rm -rf $(OBJ) $(OBJ_S)
	rm -rf *.svg core
	rm -rf *.data *.data.old

measurement-topdown: $(OBJ)
	sudo perf stat --topdown -C 3 -- taskset -c 3 chrt --fifo 99 ./$(OBJ)

measurement-ports: $(OBJ)
	sudo perf stat -D 200 -C 3 \
	  -e cycles,uops_executed.core \
	  -e uops_dispatched_port.port_0 \
	  -e uops_dispatched_port.port_1 \
	  -e uops_dispatched_port.port_2 \
	  -e uops_dispatched_port.port_3 \
	  -e uops_dispatched_port.port_4 \
	  -e uops_dispatched_port.port_5 \
	  -e uops_dispatched_port.port_6 \
	  -e uops_dispatched_port.port_7 \
	  -- taskset -c 3 chrt --fifo 99 ./$(OBJ)


measurement: measurement-topdown measurement-ports

disassembly: $(OBJ)
	objdump -drwC --no-show-raw-insn --visualize-jumps=extended-color $(OBJ)

.PHONY: all clean install measurement measurement-topdown measurement-ports
