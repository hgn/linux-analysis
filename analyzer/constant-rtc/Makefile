OBJ = constant-rtc
CFLAGS  = -g -fno-omit-frame-pointer -O0

OBJ_C = $(addsuffix .c,$(OBJ))
OBJ_S = $(addsuffix .s,$(OBJ))


$(OBJ): $(OBJ_C)
	$(CC) -Wa,-ahl=$(OBJ_S) $(CFLAGS) $< -o $@ -lpthread

clean:
	rm -rf $(OBJ) $(OBJ_S)
	rm -rf *.svg core
	rm -rf *.data *.data.old
	rm -rf stack-increase-stat.csv

disassembly: $(OBJ)
	objdump -drwC --no-show-raw-insn --visualize-jumps=extended-color $(OBJ)
