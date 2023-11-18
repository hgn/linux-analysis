CFLAGS  = -g -fno-omit-frame-pointer -O0 -Wno-div-by-zero -Wall -Wextra
LIBS = -lpthread -lm

TARGET = greedy-yielders
SRC = $(addsuffix .c, $(TARGET))

RT_SETUP = taskset -c 1 chrt --fifo 1


$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $< -o $@ $(LIBS)

analyze: $(TARGET)
	sudo perf record -C 1 -e sched:sched_switch -- $(RT_SETUP) ./$(TARGET)

analyze-full: $(TARGET)
	sudo trace-cmd record -C perf -M 2 -p function -e sched_switch -- perf record -C 1 -e sched:sched_switch,irq:\* -- $(RT_SETUP) ./$(TARGET)
	@echo trace-cmd report

clean:
	rm -rf $(TARGET)
	sudo rm -rf perf.data perf.data.old trace.dat

.PHONY: clean bootstrap analyze analyze-full bootstrap
