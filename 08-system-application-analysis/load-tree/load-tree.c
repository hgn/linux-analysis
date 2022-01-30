#include <inttypes.h>

static uint64_t pad;

#define BUSY_LOOP(x) \
do { \
	uint64_t i = x; \
	while (i--) { \
		pad ^= i; \
	}\
} while (0)

#define	LOOP_VAL_50 100000000
#define	LOOP_VAL_25 ((unsigned)(LOOP_VAL_50 / 2))

static void function_alpha_50()
{
	BUSY_LOOP(LOOP_VAL_50);
}


static void function_gamma_25_a(void)
{
	BUSY_LOOP(LOOP_VAL_25);
}

static void function_gamma_25_b(void)
{
	BUSY_LOOP(LOOP_VAL_25);
}

static void function_beta_50()
{
	function_gamma_25_a();
	function_gamma_25_b();
}


int main(void)
{
	unsigned iterations = 10;
	while (iterations--) {
		function_alpha_50();
		function_beta_50();
	}
}
