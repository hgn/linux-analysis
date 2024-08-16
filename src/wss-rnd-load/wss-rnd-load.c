#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdint.h>

#define PSEUDO_RANDOM(seed) ((seed * 0x41C64E6D + 0x3039) & 0x7FFFFFFF)

static void loader(char *memory, size_t iterations, size_t n, unsigned seed) __attribute__((noinline));

static void loader(char *memory, size_t iterations, size_t n, unsigned seed)
{
	size_t i;
	size_t index;
	volatile char value;

	for (i = 0; i < iterations; ++i) {
		seed = PSEUDO_RANDOM(seed);
		index = seed % n;
		value = memory[index];
	}
}

int main(int argc, char *argv[])
{
	size_t n;
	size_t iterations;
	char *memory;
	unsigned seed;

	if (argc != 3) {
		fprintf(stderr, "Usage: %s <number_of_bytes> <iterations>\n", argv[0]);
		return EXIT_FAILURE;
	}

	n = strtoul(argv[1], NULL, 10);
	iterations = strtoul(argv[2], NULL, 10);

	if (n <= 0 || iterations <= 0) {
		fprintf(stderr, "Both number_of_bytes and iterations must be positive integers.\n");
		return EXIT_FAILURE;
	}

	memory = malloc(n);
	if (memory == NULL) {
		perror("Failed to allocate memory");
		return EXIT_FAILURE;
	}

	printf("Memory size: %zu\n", n);
	printf("Memory area: %p - %p\n", memory, (void *)((uintptr_t)memory + n));

	if (mlockall(MCL_CURRENT | MCL_FUTURE) != 0) {
		perror("Failed to lock memory");
		free(memory);
		return EXIT_FAILURE;
	}

	memset(memory, 0, n);

	seed = (unsigned int)time(NULL);

	loader(memory, iterations, n, seed);

	free(memory);
	return EXIT_SUCCESS;
}

