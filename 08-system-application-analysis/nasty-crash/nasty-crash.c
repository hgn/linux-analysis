#include <stdlib.h>
#include <time.h>

#define CRASH_NESTING_LVL 20

static unsigned int nesting;

#define always_inline inline __attribute__((always_inline))

static void left_path(void);
static void right_path(void);

static __always_inline void crasher(void)
{
	if (nesting++ > CRASH_NESTING_LVL)
		nesting /= 0;
}

static __always_inline void pick_path(void)
{
	int value = rand() % 2;
	if (value)
		left_path();
	else
		right_path();
}

static void left_path(void)
{
	crasher();
	pick_path();
}

static void right_path(void)
{ 
	crasher();
	pick_path();
}


int main(void)
{
	srand(time(NULL));
	pick_path();
}
