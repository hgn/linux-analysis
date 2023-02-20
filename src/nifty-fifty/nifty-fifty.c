#include <stdio.h>
#include <inttypes.h>
#include <time.h>
#include <sys/types.h>
#include <unistd.h>


#define	NSEC_PER_SEC 1000000000ULL
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

static uint64_t calculated_overhead;

#define LOOPS 50
#define SLEEPTIME_NS 50000000ULL
#define BURNTIME_NS SLEEPTIME_NS

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

static void sleep_nsecs(uint64_t nsecs)
{
	struct timespec ts;

	ts.tv_nsec = nsecs % 999999999;
	ts.tv_sec = nsecs / 999999999;

	nanosleep(&ts, NULL);
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

int main(void)
{
	unsigned iterations = 50;

	calibrate_overhead();
	printf("pid: %ld\n", (long) getpid());

	while (iterations--) {
		burn_nsecs(BURNTIME_NS);
		sleep_nsecs(SLEEPTIME_NS);
	}
}
