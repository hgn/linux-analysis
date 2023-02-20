#include <inttypes.h>
#include <signal.h>
#include <sys/types.h>
#include <unistd.h>


static uint64_t pad;

#define BUSY_LOOP(x) \
do { \
	uint64_t i = x; \
	while (i--) { \
		pad ^= i; \
	}\
} while (0)

#define	LOOP_VAL_20 100000000
#define	LOOP_VAL_10 ((unsigned)(LOOP_VAL_20 / 2))
#define	LOOP_VAL_5 ((unsigned)(LOOP_VAL_20 / 4))
#define LOOP_VAL_15 (LOOP_VAL_10 + LOOP_VAL_5)
#define LOOP_VAL_25 (LOOP_VAL_20 + LOOP_VAL_5)

static void leaf(unsigned int amount)
{
	BUSY_LOOP(amount);
}

static void foo_20()
{
	BUSY_LOOP(LOOP_VAL_20);
	leaf(LOOP_VAL_25);
}

static void bar_10(void)
{
	BUSY_LOOP(LOOP_VAL_10);
	leaf(LOOP_VAL_15);
}

static void qux_10(void)
{
	BUSY_LOOP(LOOP_VAL_10);
}



int main(void)
{
	unsigned iterations = 10;
	while (iterations--) {
		foo_20();
		bar_10();
		qux_10();
	}
}
