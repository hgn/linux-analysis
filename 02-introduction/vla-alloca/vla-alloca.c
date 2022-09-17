#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#define ALLOC_SIZE 120U

void __attribute__ ((noinline)) use(char *blob)
{
	fprintf(stdout, "%s", blob);
}

void f_vla(unsigned int size, char val)
{
	char blob[size];
	blob[0] = val;
	use(blob);
}

void f_alloca(unsigned int size, char val)
{
	char *blob = alloca(size);
	blob[0] = val;
	use(blob);
}

int main(void) {
	f_vla(ALLOC_SIZE, 'a');
	f_alloca(ALLOC_SIZE, 'a');

	return EXIT_SUCCESS;
}
