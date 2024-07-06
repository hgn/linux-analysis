CFLAGS  = -g -fno-omit-frame-pointer -O0 -Wno-div-by-zero -Wall -Wextra
LIBS = -lrt

TARGET = big-pager
SRC = $(addsuffix .c, $(TARGET))

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $< -o $@ $(LIBS)

run: $(TARGET)
	./$(TARGET)

record: $(TARGET)
	sudo perf record -o /tmp/perf.data -g -e kmem:\* -- ./$(TARGET) mmap 1
	sudo chown $(USER):$(USER) /tmp/perf.data

report: $(TARGET)
	perf script --reltime -i /tmp/perf.data --fields comm,cpu,time,event
	sleep 1
	perf script --reltime -i /tmp/perf.data

clean:
	rm -rf $(TARGET)
	sudo rm -rf perf.data perf.data.old

all: $(TARGET) record report

.PHONY: clean bootstrap analyze analyze-full run
