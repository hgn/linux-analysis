CFLAGS := -Wall -Wextra -g -O0 -Wno-unused-variable -mno-red-zone

SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)
TARGET = stacktrace

.PHONY: all
all: ${TARGET}

$(TARGET): $(SRCS)
	$(CC) ${LDFLAGS} ${CFLAGS} -o $@ ${SRCS}

info: $(TARGET)
	gdb --batch --quiet -ex "r" -ex "bt" -ex "info frame" -ex "x/23i 0x555555554685" -ex "disas /m saturn" ./stacktrace

.PHONY: clean
clean:
	-${RM} ${TARGET} ${OBJS} core
