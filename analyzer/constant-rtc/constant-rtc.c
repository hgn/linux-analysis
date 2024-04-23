#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <sched.h>
#include <unistd.h>
#include <inttypes.h>

#define SLEEP_TIME 1
#define ITERATIONS 4

// Global barrier
pthread_barrier_t barrier;

typedef struct {
  long timestamp_sec[ITERATIONS];
  long timestamp_nsec[ITERATIONS];
  uint64_t tsc_value[ITERATIONS];
  int cpu_id;
} data_t;

static inline uint64_t rdtsc(void)
{
	unsigned int lo, hi;
	/* Use __rdtscp for a serializing read of the TSC=2E
	   The auxiliary variable is used to store the IA32_TSC_AUX value=2E */
	__asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi) :: "rcx");
	return ((uint64_t)hi << 32) | lo;
}

void print_data(data_t *data) {
  printf("CPU %d:\n", data->cpu_id);
  for (int i = 0; i < ITERATIONS; i++) {
    printf("  timestamp:%ld.%ld;tsc:%" PRIu64 "\n",
           data->timestamp_sec[i], data->timestamp_nsec[i], data->tsc_value[i]);
  }
}

void *thread_func(void *arg) {
  data_t *data = (data_t *)arg;
  cpu_set_t cpuset;
  CPU_ZERO(&cpuset);
  CPU_SET(data->cpu_id, &cpuset);

  if (sched_setaffinity(0, sizeof(cpuset), &cpuset) != 0) {
    perror("sched_setaffinity");
    return NULL;
  }

    int policy = SCHED_RR;
    struct sched_param param;

    // Get the maximum priority value for SCHED_RR
    int priority = sched_get_priority_max(SCHED_RR);
    if (priority == -1) {
        perror("sched_get_priority_max");
        return NULL;
    }

    param.sched_priority = priority;

    // Change the thread's scheduling policy and priority
    if (pthread_setschedparam(pthread_self(), policy, &param) != 0) {
        perror("pthread_setschedparam");
        return NULL;
    }


  for (int i = 0; i < ITERATIONS; i++) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    data->timestamp_sec[i] = ts.tv_sec;
    data->timestamp_nsec[i] = ts.tv_nsec;

    sleep(SLEEP_TIME);

    pthread_barrier_wait(&barrier);
    data->tsc_value[i] = rdtsc();
  }

  return NULL;
}

void *load_generator_thread(void *arg) {
	int j, i;
	sleep(5);
	for (j = 0; j < SLEEP_TIME * 1000000; j++)
		for (i = 0; i < 10000; i++)
			;
		
	return NULL;
}

int main() {
	int num_cores = sysconf(_SC_NPROCESSORS_CONF);
	data_t *data = malloc(sizeof(data_t) * (num_cores + 2));

	pthread_barrier_init(&barrier, NULL, num_cores);

	// Create n threads for core-bound tasks
	pthread_t threads[num_cores];
	for (int i = 0; i < num_cores; i++) {
		data[i].cpu_id = i;
		pthread_create(&threads[i], NULL, thread_func, &data[i]);
	}

	// Create 2 additional threads for CPU load generation
	pthread_t load_threads[2];
	for (int i = 0; i < 2; i++) {
		pthread_create(&load_threads[i], NULL, load_generator_thread, NULL);
	}

	// Wait for all threads to finish
	for (int i = 0; i < num_cores; i++) {
		pthread_join(threads[i], NULL);
	}
	for (int i = 0; i < 2; i++) {
		pthread_join(load_threads[i], NULL);
	}

	// Print collected data in CSV format
	printf("timestamp_sec,timestamp_nsec,cpu_id,tsc_value\n");
	for (int i = 0; i < num_cores; i++) {
		print_data(&data[i]);
	}

	free(data);
	return 0;
}

