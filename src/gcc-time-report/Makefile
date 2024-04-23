CFLAGS := -Wall -Wextra -g -O3 -ftime-trace -ftime-report
CC := clang
LIBS := -lm -lpthread

SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)
TARGET = foo-bar

.PHONY: all
all: ${TARGET}

$(TARGET): $(SRCS)
	$(CC) ${LDFLAGS} ${CFLAGS} -o $@ ${SRCS} ${LIBS}

.PHONY: clean
clean:
	-${RM} ${TARGET} ${OBJS} core *.json
