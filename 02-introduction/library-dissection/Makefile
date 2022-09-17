CC = gcc
CFLAGS = -fPIC -Wall -Wextra -g
LDFLAGS = -shared
RM = rm -f
TARGET_LIB = libexample.so

SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)

.PHONY: all
all: ${TARGET_LIB}

$(TARGET_LIB): $(OBJS)
	$(CC) ${LDFLAGS} -o $@ $^

$(SRCS:.c=.d):%.d:%.c
	$(CC) $(CFLAGS) -MM $< >$@

include $(SRCS:.c=.d)

info: $(TARGET_LIB)
	readelf --relocs  $(TARGET_LIB)

.PHONY: clean
clean:
	-${RM} ${TARGET_LIB} ${OBJS} $(SRCS:.c=.d)
