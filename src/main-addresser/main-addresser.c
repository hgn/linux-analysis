#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define SLEEP_10HZ 100000

static void foobar(void)
{
}

int main()
{
	printf("foobar %p\n", &foobar);
	while (1) {
		foobar();
		usleep(SLEEP_10HZ);
	}
	return 0;
}
