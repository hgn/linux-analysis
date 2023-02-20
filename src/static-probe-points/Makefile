

CFLAGS := -Wall -Wextra -g -O0 -I.

SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)
TARGET = static-probe-points

.PHONY: all
all: ${TARGET}

$(TARGET): $(OBJS)
	$(CC) ${CFLAGS} -o $@ $^

info: $(TARGET)
	readelf --relocs  $(TARGET)

.PHONY: clean
clean:
	-${RM} ${TARGET} ${OBJS}
	-${RM}
