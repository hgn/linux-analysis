#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>

typedef void *(*alloc_func_t)(size_t size);
typedef void (*dealloc_func_t)(void *buffer, size_t size);


static void *allocate_with_sbrk(size_t size)
{
	void *current_brk = sbrk(0);
	if (current_brk == (void *)-1) {
		perror("sbrk");
		return NULL;
	}

	if (sbrk(size) == (void *)-1) {
		perror("sbrk");
		return NULL;
	}

	return current_brk;
}

static void deallocate_with_sbrk(void *buffer, size_t size)
{
	(void) buffer;
	if (sbrk(-size) == (void *)-1) {
		perror("sbrk");
	}
}

static void *allocate_with_mmap(size_t size)
{
	void *buffer = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
	if (buffer == MAP_FAILED) {
		perror("mmap");
		return NULL;
	}
	return buffer;
}

static void deallocate_with_mmap(void *buffer, size_t size)
{
	if (munmap(buffer, size) == -1) {
		perror("munmap");
	}
}

static void *allocate_with_malloc(size_t size)
{
	void *buffer = malloc(size);
	if (!buffer) {
		perror("malloc");
		return NULL;
	}
	return buffer;
}

static void deallocate_with_malloc(void *buffer, size_t size)
{
	(void) size;

	free(buffer);
}


int main(int argc, char *argv[])
{
	if (argc != 3) {
		fprintf(stderr, "Usage: %s <mmap|sbrk|malloc> <number_of_pages>\n", argv[0]);
		return EXIT_FAILURE;
	}

	char *method = argv[1];
	int num_pages = atoi(argv[2]);
	if (num_pages <= 0) {
		fprintf(stderr, "Invalid number of pages: %d\n", num_pages);
		return EXIT_FAILURE;
	}

	size_t size;
	void *buffer;
	long pagesize;
	alloc_func_t alloc_func;
	dealloc_func_t dealloc_func;

	pagesize = sysconf(_SC_PAGESIZE);
	if (pagesize == -1) {
		perror("sysconf");
		return EXIT_FAILURE;
	}

	size = num_pages * pagesize;

	if (strcmp(method, "sbrk") == 0) {
		alloc_func = allocate_with_sbrk;
		dealloc_func = deallocate_with_sbrk;
	} else if (strcmp(method, "mmap") == 0) {
		alloc_func = allocate_with_mmap;
		dealloc_func = deallocate_with_mmap;
	} else if (strcmp(method, "malloc") == 0) {
		alloc_func = allocate_with_malloc;
		dealloc_func = deallocate_with_malloc;
	} else {
		fprintf(stderr, "Unknown method: %s\n", method);
		return EXIT_FAILURE;
	}

	sleep(1);
	buffer = alloc_func(size);
	if (!buffer) {
		fprintf(stderr, "%s allocation failed\n", method);
		return EXIT_FAILURE;
	}

	sleep(1);
	memset(buffer, 0, size);
	sleep(1);

	dealloc_func(buffer, size);
	sleep(1);

	return EXIT_SUCCESS;
}
