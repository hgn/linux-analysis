#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <inttypes.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include <pthread.h>
#include <string.h>
#include <stdbool.h>
#include <sys/random.h>

#define	NSEC_PER_SEC 1000000000ULL
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

/* 10 times: 100ms burn, 100ms sleep; 1 second each thread */
#define SLEEPTIME 100000000ULL
#define BURTIME SLEEPTIME
#define THREAD_LOOPS  10
#define NO_THREADS 4

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

static void sleep_ns(uint64_t ns)
{
	struct timespec delay = { 0, ns };
	nanosleep(&delay, NULL);
}

void *thread_start(void *args)
{
	int loops = THREAD_LOOPS;

	(void) args;

	fprintf(stderr, "Thread - PID: %u, TID: %u started\n", getpid(), gettid()); 
	while (loops--) {
		burn_nsecs(SLEEPTIME);
		sleep_ns(SLEEPTIME);
	}

	return NULL;
}

int main(void)
{
	int i;
	pthread_t pthread_id[NO_THREADS];

	calibrate_overhead();

	fprintf(stderr, "Main   - PID: %u, TID: %u\n", getpid(), gettid()); 

	for (i = 0; i < NO_THREADS; i++) {
		pthread_create(&pthread_id[i], NULL, &thread_start, NULL);
	}

	for (i = 0; i < NO_THREADS; i++) {
		 pthread_join(pthread_id[i], NULL);
	}

	return EXIT_SUCCESS;
}
