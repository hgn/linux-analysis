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

measurment: $(OBJ)
	sudo perf stat --topdown -C 3 -- taskset -c 3 $(OBJ)

disassembly: $(OBJ)
	objdump -drwC --no-show-raw-insn --visualize-jumps=extended-color $(OBJ)
