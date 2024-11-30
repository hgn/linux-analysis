CC = gcc
CFLAGS = -Wall -Wextra -g -fsanitize=address,undefined -std=gnu2x
LDFLAGS = -fsanitize=address,undefined

TARGET = xmallocer
SRCS = xmallocer.c

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET) $(LDFLAGS)

clean:
	rm -f $(TARGET) *.o

memcheck: $(TARGET)
	./$(TARGET)

