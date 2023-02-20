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
#include <unistd.h>
#include <signal.h>
#include <sched.h>
#include <assert.h>

#define MAX_THREADS 256

static void bound_to_core(int core_id)
{
	cpu_set_t mask;

	CPU_ZERO(&mask);
	CPU_SET(core_id, &mask);
	assert(sched_setaffinity(0, sizeof(mask), &mask) != -1);
}

void *thread_start(void *args)
{
	volatile uint64_t cnt;
	int no;
	no = (int)args;

	fprintf(stderr, "bound to %d\n", no); 
	bound_to_core(no);

	while (1) {
		cnt += 1;
	}

	return NULL;
}

int main(void)
{
	int i;
	pthread_t pthread_id[MAX_THREADS];
	int online_cpus;


	online_cpus = sysconf(_SC_NPROCESSORS_ONLN);

	for (i = 0; i < online_cpus; i++) {
		fprintf(stderr, "Start Thread %d\n", i + 1); 
		pthread_create(&pthread_id[i], NULL, &thread_start, (void *)i);
		sleep(3);
	}

	sleep(120);

	for (i = 0; i < online_cpus; i++) {
		 pthread_kill(pthread_id[i], SIGKILL);
	}

	sleep(1);

	return EXIT_SUCCESS;
}
