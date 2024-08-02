OBJ = asm-mem-load-store
CFLAGS  = -g -fno-omit-frame-pointer -O0 -Wall -Wextra

OBJ_C = $(addsuffix .c,$(OBJ))
OBJ_S = $(addsuffix .s,$(OBJ))


$(OBJ): $(OBJ_C)
	$(CC) $(CFLAGS) $< -o $@

info: $(OBJ)
	objdump --section=.text --disassemble=main --no-show-raw-insn --visualize-jumps=color $(OBJ)
	sudo perf stat -e mem_inst_retired.all_loads,mem_inst_retired.all_stores -- ./$(OBJ)


clean:
	rm -rf $(OBJ)
	rm -rf *.data *.data.old

all: $(OBJ)
