

CFLAGS := -Wall -Wextra -g -Og -I.

SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)
TARGET = outer-inner

.PHONY: all
all: ${TARGET}

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) ${LDFLAGS} -o $@ $^

info: $(TARGET)
	readelf --relocs  $(TARGET)

.PHONY: clean
clean:
	-${RM} ${TARGET} ${OBJS}
