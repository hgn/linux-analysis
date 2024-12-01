CC = gcc
CFLAGS = -shared -fPIC -Wall -O2 -pthread
TARGET = mallinfo.so
SRC = mallinfo.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

test:
	LD_PRELOAD=./$(TARGET) inkscape

.PHONY: all clean test

