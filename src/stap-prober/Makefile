OBJ = stap-prober
CFLAGS  = -g -fno-omit-frame-pointer -O3 -Wall -Wextra

OBJ_C = $(addsuffix .c,$(OBJ))
OBJ_S = $(addsuffix .s,$(OBJ))


$(OBJ): $(OBJ_C)
	$(CC) $(CFLAGS) $< -o $@

info: $(OBJ)
	objdump -d -M att --no-show-raw-insn --disassemble=main $(OBJ)
	readelf -n stap-prober | grep -A 6 .note.stapsdt -


record:
	-@sudo perf probe --del 'sdt_test:*'
	sudo perf buildid-cache -v --add ./$(OBJ)
	sudo perf list sdt
	sudo perf probe -x ./$(OBJ) %sdt_test:main
	sudo perf record -e sdt_test:main ./$(OBJ)
	-@sudo perf probe --del 'sdt_test:*'
	sudo chown $$USER perf.data
	perf script -F -comm,-cpu,-tid,-ip,-addr --deltatime
	rm -rf perf.data

clean:
	rm -rf $(OBJ)
	rm -rf *.data *.data.old

all: $(OBJ)
