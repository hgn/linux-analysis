#include <stdio.h>
#include <string.h>

#define SMASH_INCREMENT 1024
#define PEAK_WORK (1024 * 1024)


static void smash(size_t smash_size)
{
	char pad[smash_size];

	memset(pad, 0, smash_size);
}


int main(void)
{
	size_t i = 0;

	do {
		fprintf(stderr, "\rsmash stack now with %zu byte", i);
		smash(i);
		i += SMASH_INCREMENT; 
	} while (42);
}

