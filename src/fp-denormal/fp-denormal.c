#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <xmmintrin.h>
#include <time.h>
#include <math.h>

#define ITERATIONS 1000000000

int main(int argc, char **argv)
{
	volatile float a, b, c;
	unsigned int i;
	clock_t start, end;
	double elapsed;

	if (argc != 2) {
		printf("error: <denormal | normal> as argument\n");
		return 1;
	}

	if (strcmp(argv[1], "denormal") != 0 && strcmp(argv[1], "normal") != 0) {
		printf("error: <denormal | normal> as argument\n");
		return 1;
	}


	b = 2.0f;

	if (!strcmp(argv[1], "denormal")) {
		a = 1.0e-40f;
		printf("Running with denormal value: %e\n", a);
	} else {
		a = 1.0e-10f;
		printf("Running with normal value: %e\n", a);
	}

	start = clock();

	for (i = 0; i < ITERATIONS; i++)
		c = a * b;

	end = clock();
	elapsed = (double)(end - start) / CLOCKS_PER_SEC;

	printf("Done. Elapsed time: %.6f seconds\n", elapsed);
	printf("Final result: %.30e\n", c);

	return 0;
}

