#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>


void *thread_start(void *args)
{
	fprintf(stderr, "Thread - PID: %u, TID: %u\n", getpid(), gettid()); 
	while (1)
		;
}

int main(void)
{
	pthread_t pthread_id;

	fprintf(stderr, "Main   - PID: %u, TID: %u\n", getpid(), gettid()); 

	pthread_create(&pthread_id, NULL, &thread_start, NULL);

	while (1)
		;
}
