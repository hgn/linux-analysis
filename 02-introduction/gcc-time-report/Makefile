CFLAGS := -Wall -Wextra -g -O0 -ftime-report

SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)
TARGET = foo-bar

.PHONY: all
all: ${TARGET}

$(TARGET): $(SRCS)
	$(CC) ${LDFLAGS} ${CFLAGS} -o $@ ${SRCS}

.PHONY: clean
clean:
	-${RM} ${TARGET} ${OBJS} core
