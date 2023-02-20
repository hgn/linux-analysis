

CFLAGS := -Wall -Wextra -g -O1

SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)
TARGET = vla-alloca

.PHONY: all
all: ${TARGET}

$(TARGET): $(OBJS)
	$(CC) ${LDFLAGS} -o $@ $^

info: $(TARGET)
	readelf --relocs  $(TARGET)

.PHONY: clean
clean:
	-${RM} ${TARGET} ${OBJS}
