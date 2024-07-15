OBJ = dee-dum-prober
CFLAGS  = -g -fno-omit-frame-pointer -O0 -Wall -Wextra

OBJ_C = $(addsuffix .c,$(OBJ))
OBJ_S = $(addsuffix .s,$(OBJ))


$(OBJ): $(OBJ_C)
	$(CC) $(CFLAGS) $< -o $@

info: $(OBJ)
	sudo perf probe -x ./$(OBJ) --funcs
	sudo perf probe -x ./$(OBJ) --vars swap_dum
	sudo perf probe -x ./$(OBJ) --line swap_dum
	sudo perf probe -x ./$(OBJ) --vars swap_dum:3


record:
	-@sudo perf probe --del '*'
	-@sudo perf probe -x ./$(OBJ) --add 'swap_dum_prologe=swap_dum t->dum:x64'
	-@sudo perf probe -x ./$(OBJ) --add 'swap_dum_middle=swap_dum:4 prev_dum=prev_dum new_dum=t->dum dee=t->dee'
	-@sudo perf probe -x ./$(OBJ) --add 'swap_dum_epilog=swap_dum%return $$retval'
	-@sudo perf record -e 'probe_dee:*' -R -- ./$(OBJ)
	-@sudo perf probe --del '*'
	-@sudo chown $$USER perf.data
	-@perf script -F -comm,-cpu,-tid,-ip,-addr --deltatime

clean:
	rm -rf $(OBJ)
	rm -rf *.data *.data.old

all: $(OBJ)
