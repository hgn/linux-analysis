OBJ = wss-rnd-load
CFLAGS  = -g -fno-omit-frame-pointer -O2 -Wall -Wextra

OBJ_C = $(addsuffix .c,$(OBJ))
OBJ_S = $(addsuffix .s,$(OBJ))


$(OBJ): $(OBJ_C)
	$(CC) $(CFLAGS) $< -o $@

info: $(OBJ)
	objdump --section=.text --disassemble=loader --no-show-raw-insn --visualize-jumps=color $(OBJ)
	sudo perf stat -e mem_inst_retired.all_loads,mem_inst_retired.all_stores -- ./$(OBJ) 1 1000000000


clean:
	rm -rf $(OBJ)
	rm -rf *.data *.data.old

all: $(OBJ)
