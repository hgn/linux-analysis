CFLAGS  = -g -fno-omit-frame-pointer -O0 -Wno-div-by-zero -Wall -Wextra
LIBS = -lpthread -lm

TARGET = greedy-yielders
SRC = $(addsuffix .c, $(TARGET))

RT_SETUP = taskset -c 1 chrt --rr 23

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $< -o $@ $(LIBS)

run: $(TARGET)
	sudo $(RT_SETUP) ./$(TARGET)

analyze: $(TARGET)
	sudo perf record -C 1 -e sched:sched_switch -- $(RT_SETUP) ./$(TARGET)

analyze-full: $(TARGET)
	sudo trace-cmd record -C perf -M 2 -p function -e sched_switch -- sudo perf record -C 1 -e sched:sched_switch -- $(RT_SETUP) ./$(TARGET)
	@echo trace-cmd report

clean:
	rm -rf $(TARGET)
	sudo rm -rf perf.data perf.data.old trace.dat

all: $(TARGET)

.PHONY: clean bootstrap analyze analyze-full run
