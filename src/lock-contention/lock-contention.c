#define _GNU_SOURCE
#include <pthread.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_THREADS 4
#define LOOP_COUNT  1000000

static pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
static unsigned int result = 0;

static void *worker(void *arg)
{
	unsigned int loop = LOOP_COUNT;
	(void)arg;

	while (loop--) {
		unsigned int calc = (unsigned int)(sin((double)loop) * 1000.0);
		pthread_mutex_lock(&mutex);
		result += calc;
		pthread_mutex_unlock(&mutex);
	}

	return NULL;
}

int main(void)
{
	pthread_t threads[NUM_THREADS];
	int i;

	for (i = 0; i < NUM_THREADS; i++) {
		if (pthread_create(&threads[i], NULL, worker, NULL)) {
			perror("pthread_create");
			exit(EXIT_FAILURE);
		}
	}

	for (i = 0; i < NUM_THREADS; i++) {
		pthread_join(threads[i], NULL);
	}

	printf("Result: %u\n", result);

	return 0;
}

