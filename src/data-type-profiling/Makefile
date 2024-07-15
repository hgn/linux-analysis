OBJ = data-type-profiling
CFLAGS  = -g -fno-omit-frame-pointer -O0 -Wall

OBJ_C = $(addsuffix .c,$(OBJ))
OBJ_S = $(addsuffix .s,$(OBJ))


$(OBJ): $(OBJ_C)
	$(CC) $(CFLAGS) $< -o $@

record:
	sudo perf record -C 1 -e '{cpu_core/mem-stores/P}' -- taskset -c 1 ./skbuff-berserk
	#sudo perf record -C 1 -e '{cpu_core/mem-loads,ldlat=30/P,cpu_core/mem-stores/P}' -- taskset -c 1 ./skbuff-berserk
	#sudo perf record -C 1 -e '{cpu_core/mem-loads,ldlat=30/P}' -- taskset -c 1 ./skbuff-berserk
	sudo chown $$USER perf.data

clean:
	rm -rf $(OBJ)
	rm -rf *.data *.data.old

all: $(OBJ)
