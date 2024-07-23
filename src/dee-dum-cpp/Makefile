OBJ = dee-dum-cpp
CXX = g++
SRC = dee-dum-cpp.cc

all: $(OBJ)

$(OBJ): $(SRC)
	$(CXX) -g -O0 -Wall -o $(OBJ) $(SRC)


info: $(OBJ)
	sudo perf probe -x ./$(OBJ) --funcs --no-demangle | grep dee_dum -
	sudo perf probe -x ./$(OBJ) --vars swap_dum
	sudo perf probe -x ./$(OBJ) --line swap_dum
	sudo perf probe -x ./$(OBJ) --vars swap_dum:2


record: $(OBJ)
	-@sudo perf probe --del '*'
	sudo perf probe -x ./$(OBJ) --add 'swap_dum_prologe=swap_dum t->dum:x64'
	sudo perf probe -x ./$(OBJ) --add 'swap_dum_middle=swap_dum:2 prev_dum=prev_dum new_dum=t->dum dee=t->dee'
	#sudo perf probe -x ./$(OBJ) --add 'swap_dum%return $$retval'
	sudo perf record -e 'probe_dee:*' -R -- ./$(OBJ)
	sudo perf probe --del '*'
	sudo chown $$USER perf.data
	perf script -F -comm,-cpu,-tid,-ip,-addr --deltatime

clean:
	rm -rf $(OBJ)
	rm -rf *.data *.data.old

all: $(OBJ)
