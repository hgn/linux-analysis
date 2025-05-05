#include <stdint.h>

int main()
{
	volatile uint64_t counter = 0;
	const uint64_t limit = 0x2540be3ff;

	while (1) {
		__asm__ volatile("nop");
		counter++;
		if (counter >= limit)
			break;
	}

	return 0;
}
