OBJ = fp-denormal
CFLAGS  = -Wall -Wextra -funwind-tables -Wall -Wextra -std=gnu99 -fno-omit-frame-pointer -O0 -g

OBJ_C = $(addsuffix .c,$(OBJ))
OBJ_S = $(addsuffix .s,$(OBJ))


$(OBJ): $(OBJ_C)
	$(CC) -Wa,-ahl=$(OBJ_S) $(CFLAGS) $< -o $@

clean:
	rm -rf $(OBJ) $(OBJ_S)
	rm -rf *.svg core
	rm -rf *.data *.data.old

disassembly: $(OBJ)
	objdump -drwC --no-show-raw-insn --visualize-jumps=extended-color $(OBJ)

record: $(OBJ)
	sudo rm -rf perf*.data
	sudo perf record -e assists.fp:uP  -o perf-denormal.data -- taskset -c 6 ./$(OBJ) denormal
	sudo perf record -e assists.fp:uP  -o perf-normal.data   -- taskset -c 6 ./$(OBJ) normal
	sudo chown $$USER perf*.data

report:
	perf annotate --stdio -i perf-denormal.data | grep -C 4 mulss -
