CC = gcc
CFLAGS = -Wall -Wextra -pedantic -O2

TARGET = page-toucher
SRC = page-toucher.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $^

run: $(TARGET)
	sudo ./page-idle-wss.py -- ./page-toucher -n 100 -a 100 -s 5

clean:
	rm -f $(TARGET)

.PHONY: all clean run

