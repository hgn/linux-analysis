CFLAGS  = -g -fno-omit-frame-pointer -O0 -Wno-div-by-zero -Wall -Wextra
LIBS = -lrt

TARGET = main-addresser
SRC = $(addsuffix .c, $(TARGET))

RT_SETUP = taskset -c 1

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $< -o $@ $(LIBS)

run: $(TARGET)
	sudo $(RT_SETUP) ./$(TARGET)

analyze: $(TARGET)
	sudo perf record -o /tmp/perf.data -C 1 -e timer:\* -- $(RT_SETUP) ./$(TARGET)
	sudo chown $(USER):$(USER) /tmp/perf.data

clean:
	rm -rf $(TARGET)
	sudo rm -rf perf.data perf.data.old

all: $(TARGET)

.PHONY: clean bootstrap analyze analyze-full run
