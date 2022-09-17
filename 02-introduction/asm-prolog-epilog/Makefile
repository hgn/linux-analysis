CFLAGS := -Wall -Wextra -g -O0 -mno-red-zone
EXTRA_ASM_FLAGS := -fverbose-asm

SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)
ASM_OBJ = $(SRCS:.c=.s)
TARGET = prolog-epilog

.PHONY: all
all: ${TARGET}

$(TARGET): $(OBJS)
	$(CC) ${LDFLAGS} ${CFLAGS} -Wa,-adhln=${ASM_OBJ} -c -o $@ ${SRCS}

info: $(TARGET)
	readelf --relocs $(TARGET)
	objcopy -I elf64-x86-64 -j .text -O binary prolog-epilog.o prolog-epilog.text.bin
	readelf -x .text prolog-epilog.o

.PHONY: clean
clean:
	-${RM} ${TARGET} ${OBJS} ${ASM_OBJ}
