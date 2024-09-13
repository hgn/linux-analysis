OBJ = /usr/bin/sleep 0.1

CORE = 14

# for deadline
RUNTIME_NS = 1000000      # 1ms
DEADLINE_NS = 5000000     # 5ms
PERIOD_NS = 5000000       # 5ms

record:
	rm -rf *.log
	# Run with SCHED_OTHER (nice 0)
	@echo "Recording with SCHED_OTHER (nice 0)..."
	sudo perf record -C $(CORE) -e sched:sched_switch -- taskset -c $(CORE) chrt --other 0 nice -n 0 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-other-0-0.log

	# Run with SCHED_OTHER (min nice 19)
	@echo "Recording with SCHED_OTHER (min nice 19)..."
	sudo perf record -C $(CORE) -e sched:sched_switch -- taskset -c $(CORE) chrt --other 0 nice -n 19 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-other-0-19.log

	# Run with SCHED_OTHER (max nice -20)
	@echo "Recording with SCHED_OTHER (max nice -20)..."
	sudo perf record -C $(CORE) -e sched:sched_switch -- taskset -c $(CORE) chrt --other 0 nice -n -20 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-other-0--20.log

	# Run with SCHED_BATCH (nice 0)
	@echo "Recording with SCHED_BATCH (nice 0)..."
	sudo perf record -C $(CORE) -e sched:sched_switch -- taskset -c $(CORE) chrt --batch 0 nice -n 0 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-batch-0-0.log

	# Run with SCHED_BATCH (min nice 19)
	@echo "Recording with SCHED_BATCH (min nice 19)..."
	sudo perf record -C $(CORE) -e sched:sched_switch -- taskset -c $(CORE) chrt --batch 0 nice -n 19 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-batch-0-19.log

	# Run with SCHED_BATCH (max nice -20)
	@echo "Recording with SCHED_BATCH (max nice -20)..."
	sudo perf record -C $(CORE) -e sched:sched_switch -- taskset -c $(CORE) chrt --batch 0 nice -n -20 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-batch-0--20.log

	# Run with SCHED_IDLE (no priority)
	@echo "Recording with SCHED_IDLE..."
	sudo perf record -C $(CORE) -e sched:sched_switch -- taskset -c $(CORE) chrt --idle 0 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-idle-0-0.log

	# Run with SCHED_FIFO (min priority 1)
	@echo "Recording with SCHED_FIFO (min priority 1)..."
	sudo perf record -C $(CORE) -e sched:sched_switch -- taskset -c $(CORE) chrt --fifo 1 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-fifo-1-0.log

	# Run with SCHED_FIFO (max priority 99)
	@echo "Recording with SCHED_FIFO (max priority 99)..."
	sudo perf record -C $(CORE) -e sched:sched_switch -- taskset -c $(CORE) chrt --fifo 99 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-fifo-99-0.log

	# Run with SCHED_RR (min priority 1)
	@echo "Recording with SCHED_RR (min priority 1)..."
	sudo perf record -C $(CORE) -e sched:sched_switch -- taskset -c $(CORE) chrt --rr 1 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-rr-1-0.log

	# Run with SCHED_RR (max priority 99)
	@echo "Recording with SCHED_RR (max priority 99)..."
	sudo perf record -C $(CORE) -e sched:sched_switch -- taskset -c $(CORE) chrt --rr 99 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-rr-99-0.log

	# Run with SCHED_DEADLINE
	@echo "Recording with SCHED_DEADLINE... (cannot pin to core and deadline)"
	sudo perf record -a -e sched:sched_switch -- chrt --deadline --sched-runtime $(RUNTIME_NS) --sched-deadline $(DEADLINE_NS) --sched-period $(PERIOD_NS) 0 $(OBJ)
	sudo perf script --fields trace | egrep "sleep.*==>" - | head -n 1 > policy-deadline-0-0.log

show:
	grep . *.log | column -t -s ":"

clean:
	rm -rf *.data *.data.old
	rm -rf *.log

all: record show

