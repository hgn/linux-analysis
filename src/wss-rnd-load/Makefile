OBJ = wss-rnd-load
CFLAGS  = -g -fno-omit-frame-pointer -O0 -Wall -Wextra

OBJ_C = $(addsuffix .c,$(OBJ))
OBJ_S = $(addsuffix .s,$(OBJ))

DATADIR = data
CACHE_EVENTS = cpu_core/mem_inst_retired.all_loads/u,cpu_core/mem_load_retired.l1_hit/u,cpu_core/mem_load_retired.l1_miss/u,cpu_core/mem_load_retired.l2_hit/u,cpu_core/mem_load_retired.l2_miss/u,cpu_core/mem_load_retired.l3_hit/u,cpu_core/mem_load_retired.l3_miss/u

MEM_EVENTS = {cpu_core/mem-loads-aux/u,cpu_core/mem-loads,ldlat=1/uP}:S

CPU = 15

PERF_STAT = perf stat --repeat 10 -C $(CPU)
PERF_RECORD_MEM = perf record --weight --data -C $(CPU) -d

WORKLOAD = chrt --fifo 1 taskset -c $(CPU) ./$(OBJ)

## Alder Lake Setup (12900k)
## L1D: 49152 (48 KB)
## L2:  2097152 (2 MB)
## L3: 37748736 (36 MB)
# SIZES = 1 49152 2097152 37748736 4294967296
# these are the cache values, dicived by 2, fitting in cache
SIZES = 1 24576 1048576 18874368 4294967296

$(OBJ): $(OBJ_C)
	$(CC) $(CFLAGS) $< -o $@

run: $(OBJ)
	@rm -rf $(DATADIR)
	@mkdir $(DATADIR)
	sudo $(PERF_STAT) -e mem_inst_retired.all_loads:u -- $(WORKLOAD) 1 1000000000
	sudo $(PERF_STAT) -e mem_inst_retired.all_loads:u,cache-references:u,cache-misses:u -- $(WORKLOAD) 18874368 1000000000
	sudo $(PERF_STAT) -e cpu_core/mem_inst_retired.all_loads/u,cpu_core/L1-dcache-loads/u,cpu_core/L1-dcache-load-misses/u,cpu_core/LLC-loads/u,cpu_core/LLC-load-misses/u -- $(WORKLOAD) 18874368 1000000000
	echo -e "\n\n"

	#objdump --section=.text --disassemble=loader --no-show-raw-insn --visualize-jumps=color $(OBJ)
	#sudo $(PERF_STAT) -e cpu_core/mem_inst_retired.all_loads/,cpu_core/mem_load_retired.l1_hit/ --  $(WORKLOAD) 1 1000000000
	$(foreach size,$(SIZES), \
					echo "\n\n$(PERF_STAT) -e $(CACHE_EVENTS) --  $(WORKLOAD) $(size) 1000000000"; \
					sudo $(PERF_STAT) -e $(CACHE_EVENTS) --  $(WORKLOAD) $(size) 1000000000; )

	$(foreach size,$(SIZES), \
					echo "\n\n$(PERF_RECORD_MEM) -e $(MEM_EVENTS) -o $(DATADIR)/perf-$(size).data -- $(WORKLOAD) $(size) 10000000000"; \
					sudo $(PERF_RECORD_MEM) -e $(MEM_EVENTS) -o $(DATADIR)/perf-$(size).data -- $(WORKLOAD) $(size) 10000000000;)

	$(foreach size,$(SIZES), \
					echo "\n\nperf mem -t load report -i $(DATADIR)/perf-$(size).data --sort=mem --stdio" \
					sudo perf mem -t load report -i $(DATADIR)/perf-$(size).data --sort=mem --stdio;)
	#perf report script -i data/perf-1.data
	#perf report -i data/perf-1.data --dump-raw-trace



clean:
	rm -rf $(OBJ)
	rm -rf *.data *.data.old

all: run

.PHONY: all run
