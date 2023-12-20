#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int main(int ac, char **av)
{
	unsigned int i = 500000;
	struct timespec ts;

	(void) ac; (void) av;

	ts.tv_sec = 0;
	ts.tv_nsec = 1;

	while (i--) {
		nanosleep(&ts, NULL);
	}

	return 0;
}
