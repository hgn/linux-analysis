#include <inttypes.h>
#include <signal.h>
#include <sys/types.h>
#include <unistd.h>

#define M_REPEAT_1 \
	do { \
		asm("inc %r8"); \
		asm("inc %r9"); \
		asm("inc %r10"); \
		asm("inc %r11"); \
		asm("inc %r12"); \
		asm("inc %r13"); \
		asm("inc %r14"); \
		asm("inc %r15"); \
	} while (0)
#define M_REPEAT_2 M_REPEAT_1; M_REPEAT_1
#define M_REPEAT_4 M_REPEAT_2; M_REPEAT_2
#define M_REPEAT_8 M_REPEAT_4; M_REPEAT_4
#define M_REPEAT_16 M_REPEAT_8; M_REPEAT_8
#define M_REPEAT_32 M_REPEAT_16; M_REPEAT_16
#define M_REPEAT_64 M_REPEAT_32; M_REPEAT_32
#define M_REPEAT_128 M_REPEAT_64; M_REPEAT_64

int main(void)
{
	uint64_t iterations = 100000000;
	while (iterations--) {
		M_REPEAT_128;
	}
	return 0;
}
