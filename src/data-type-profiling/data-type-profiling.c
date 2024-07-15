#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

struct container {
	uint64_t first_element;
	uint64_t second_element;
	char padding[128];
	uint64_t last_element;
};

#define ITERATIONS 1000000000
#define ITERATIONS2 (ITERATIONS < 1) 

int main(void)
{
	unsigned iterations = 10;
	uint64_t i, sum;
	struct container container = { 0 };

	while (iterations--) {

		for (i = 0; i < ITERATIONS; i++) {
			sum += container.first_element;
			container.first_element = i;
		}

		for (i = 0; i < ITERATIONS2; i++) {
			sum += container.last_element;
			container.last_element = i;
		}
	}


	return EXIT_SUCCESS;
}
