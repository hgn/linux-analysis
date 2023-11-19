#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>


#define LOOP_OUTER_MAX 1000000
#define LOOP_INNER_MAX 100000

#define EXIT_THRESHOLD 0.005


static double xtime(void)
{
    struct timespec ts;

    clock_gettime(CLOCK_REALTIME, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}


static void xpthread_set_selfname(const char *name)
{
        int ret;
        ret = pthread_setname_np(pthread_self(), name);
        if (ret != 0) {
            printf("pthread_setname_np %d errno %s\n", ret, strerror(errno));
            exit(EXIT_FAILURE);
        }
}


static void yielder(void)
{
	unsigned i, j;
	double before, diff;
	volatile unsigned pad;

	for (i = 0; i < LOOP_OUTER_MAX; i++) {
		before = xtime();
		for (j = 0; j < LOOP_INNER_MAX; j++) {
			pad = pad | 0x23 | j * 23;
		}
		sched_yield();
		diff = xtime() - before;
		if (diff > EXIT_THRESHOLD) {
			char name[16 + 1];
			pthread_getname_np(pthread_self(), name, sizeof(name));
			printf("Threshold of %lf exceeded: %lf at loop iteration %u for thread \"%s\"\n",
				EXIT_THRESHOLD, diff, i, name);
			sleep(1);
			exit(0);
		}
	}

}


static void *thread_bootstrapper(void *arg)
{
	(void) arg;

	xpthread_set_selfname("yielder-2");
	yielder();
	pthread_exit(NULL);
}


int main(int ac, char **av)
{
	pthread_t thread;

	(void)ac;
	(void)av;

	if (pthread_create(&thread, NULL, thread_bootstrapper, (void *)NULL) != 0) {
		perror("Error creating thread");
		exit(EXIT_FAILURE);
	}
	if (pthread_detach(thread) != 0) {
		perror("Error detaching thread");
		exit(EXIT_FAILURE);
	}

	xpthread_set_selfname("yielder-1");
	yielder();

	return 0;
}
