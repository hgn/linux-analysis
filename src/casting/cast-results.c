#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <limits.h>

#define TRUE_FALSE(exp) \
({                                        \
    if (exp)                              \
        fprintf(stderr, "true\n");        \
    else                                  \
        fprintf(stderr, "false\n");       \
})

static void true_false_tests(void)
{
	TRUE_FALSE(-1 < 1U);
}

static void int8_propagation(void)
{
	int8_t val1 = 100;
	int8_t val2 = 3;
	int8_t val3 = 4;
	int8_t result = val1 * val2 / val3;
	fprintf(stderr, "val1 * val2 / val3 -> %d\n", result);
}

static void int_propagation(void)
{
	unsigned val1 = UINT_MAX;
	unsigned val2 = 4;
	unsigned val3 = 8;
	unsigned result = val1 * (long long)val2 / val3;
	fprintf(stderr, "%u * %u / %u -> %u (UINT_MAX: %u) \n", val1, val2, val3, result, UINT_MAX);
}

static void char_comp(void)
{
	char a = 0xff;
	unsigned char b = 0xff;
	if (a == b)
		fprintf(stderr, "identical\n");
	else
		fprintf(stderr, "NOT identical\n");
}


int main(void)
{
	true_false_tests();
	int8_propagation();
	char_comp();
	int_propagation();

}
