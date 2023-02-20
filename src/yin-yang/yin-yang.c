#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <time.h>
#include <sys/types.h>
#include <sys/eventfd.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>


#define	NSEC_PER_SEC 1000000000ULL
#define MIN(x, y) (((x) < (y)) ? (x) : (y))
#define BURNTIME_NS 100000000ULL /* 100 ms */

static uint64_t calculated_overhead;


static uint64_t get_nsecs(void)
{
	struct timespec ts;

	clock_gettime(CLOCK_MONOTONIC, &ts);

	return ts.tv_sec * NSEC_PER_SEC + ts.tv_nsec;
}


static void burn_nsecs(uint64_t nsecs)
{
	uint64_t t0 = get_nsecs(), t1;

	do {
		t1 = get_nsecs();
	} while (t1 + calculated_overhead < t0 + nsecs);
}


static void calibrate_overhead(void)
{
	uint64_t t0, t1, delta, min_delta = NSEC_PER_SEC;
	int i;

	for (i = 0; i < 10; i++) {
		t0 = get_nsecs();
		burn_nsecs(0);
		t1 = get_nsecs();
		delta = t1 - t0;
		min_delta = MIN(min_delta, delta);
	}
	calculated_overhead = min_delta;

	printf("run measurement overhead: %" PRIu64 " nsecs\n", min_delta);
}


static void yin_yang(const char *who, int readpipe, int writepipe)
{
	uint64_t retval;

	while (42) {
		read(readpipe, &retval, sizeof(uint64_t));
		printf("%s read number %"PRIu64" from eventfd\n", who, retval);
		burn_nsecs(BURNTIME_NS);
		retval--;
		write(writepipe, &retval, sizeof(uint64_t));
		if (retval <= 0)
			break;
	}
	write(writepipe, &retval, sizeof(uint64_t));
	exit(EXIT_SUCCESS);
}


int main(void)
{
	uint64_t init_val = 24;
	int yin, yang;

	calibrate_overhead();

	yin  = eventfd(0, 0);
	yang = eventfd(0, 0);

	/* we start be triggering yang */
	write(yang, &init_val, sizeof(uint64_t));

	switch (fork()) {
	case 0:
		printf("yang pid: %ld\n", (long) getpid());
		yin_yang("yang", yang, yin);

	default:
		printf("yin  pid: %ld\n", (long) getpid());
		yin_yang("yin ", yin, yang);
	}
}
