CFLAGS  = -g -fno-omit-frame-pointer -O0 -Wno-div-by-zero -Wall -Wextra

TARGET = turbulent-sleeper
SRC = $(addsuffix .c, $(TARGET))

RT_SETUP = taskset -c 1

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $< -o $@

run: $(TARGET)
	sudo $(RT_SETUP) ./$(TARGET)

analyze: $(TARGET)
	sudo perf record -o /tmp/perf.data -C 1 -e timer:hrtimer_init,timer:hrtimer_cancel,timer:timer_init,timer:timer_init -- $(RT_SETUP) ./$(TARGET)
	sudo chown $(USER):$(USER) /tmp/perf.data

clean:
	rm -rf $(TARGET)
	sudo rm -rf perf.data perf.data.old

all: $(TARGET)

.PHONY: clean bootstrap analyze analyze-full run
