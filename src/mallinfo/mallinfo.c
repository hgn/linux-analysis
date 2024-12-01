#define _GNU_SOURCE
#include <malloc.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

void* log_mallinfo(void* arg)
{
	struct mallinfo2 mi;
	pthread_setname_np(pthread_self(), "mallinfo");
	while (1) {
		mi = mallinfo2();
		fprintf(stderr, "Mallinfo2:\n");
		fprintf(stderr, "  arena: %zu bytes\n", mi.arena);
		fprintf(stderr, "  ordblks: %zu (number of free blocks)\n", mi.ordblks);
		fprintf(stderr, "  smblks: %zu (number of small blocks)\n", mi.smblks);
		fprintf(stderr, "  hblks: %zu (number of mmap regions)\n", mi.hblks);
		fprintf(stderr, "  hblkhd: %zu bytes (space in mmap regions)\n", mi.hblkhd);
		fprintf(stderr, "  usmblks: %zu bytes (space in free small blocks)\n", mi.usmblks);
		fprintf(stderr, "  fsmblks: %zu bytes (space in fastbins)\n", mi.fsmblks);
		fprintf(stderr, "  uordblks: %zu bytes (total allocated space)\n", mi.uordblks);
		fprintf(stderr, "  fordblks: %zu bytes (total free space)\n", mi.fordblks);
		fprintf(stderr, "  keepcost: %zu bytes (top-most releasable block)\n", mi.keepcost);
		fflush(stderr);
		sleep(1);
	}
	return NULL;
}

__attribute__((constructor)) void init_logger()
{
	pthread_t thread;
	pthread_create(&thread, NULL, log_mallinfo, NULL);
	pthread_detach(thread);
}

