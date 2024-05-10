CFLAGS  = -g -fno-omit-frame-pointer -O0 -Wno-div-by-zero -Wall -Wextra
LIBS = -lm

TARGET = perf-event-open-hello-world
SRC = $(addsuffix .c, $(TARGET))

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $< -o $@ $(LIBS)

clean:
	rm -rf $(TARGET)
	sudo rm -rf perf.data perf.data.old

dependencies:
	sudo apt install libpfm4-dev

all: $(TARGET)

.PHONY: clean
