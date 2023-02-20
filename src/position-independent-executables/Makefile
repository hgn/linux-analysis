CC = gcc
CFLAGS = -fPIC -Wall -Wextra -g
LDFLAGS = -shared
RM = rm -f
TARGET_LIB = libexample.so
TARGET_ARCHIVE = libstatic.a
TARGET_APP = program

SRCS = example.c
OBJS = $(SRCS:.c=.o)

.PHONY: all
all: ${TARGET_LIB} ${TARGET_APP}

$(TARGET_APP): $(TARGET_LIB) $(TARGET_ARCHIVE)
	$(CC) -fPIE -pie -I.. -I. -L. program.c -lexample -o program
	$(CC) -I. program.c $(TARGET_ARCHIVE) -o program-static

$(TARGET_ARCHIVE): $(OBJS)
	$(AR) rcs $@ $^

$(TARGET_LIB): $(OBJS)
	$(CC) ${LDFLAGS} -o $@ $^

$(SRCS:.c=.d):%.d:%.c
	$(CC) $(CFLAGS) -MM $< >$@

include $(SRCS:.c=.d)

info: $(TARGET_LIB)
	readelf --relocs  $(TARGET_LIB)

run: ${TARGET_APP}
	 LD_LIBRARY_PATH='.' ./program

.PHONY: clean run
clean:
	-${RM} ${TARGET_LIB} ${OBJS} $(SRCS:.c=.d) ${TARGET_APP}
