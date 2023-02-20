#include <stdio.h>
#include <inttypes.h>
#include <string.h>

// for IACA markers
#include "iacaMarks.h"

#define	ARRAY_SIZE 4096

static volatile uint64_t array[ARRAY_SIZE];

__attribute__((noinline))
uint64_t array_add_loop(void)
{
	unsigned i, j;
	uint64_t sum = 0;
	//__asm__ __volatile__("# LLVM-MCA-BEGIN outer");

	for (j = 0; j < 10000000; j++)
		//#pragma unroll(32)
		IACA_START
		for (i = 0; i < ARRAY_SIZE; i++)
			sum += array[i];
		IACA_END
	//__asm__ __volatile__("# LLVM-MCA-END");
	
	return sum;
}

#if 1
int main(void)
{
	return array_add_loop();
}
#endif
