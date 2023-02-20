#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <inttypes.h>
#include <string.h>


#define	LOOPS 5000
#define BUFSIZE 10000000

uint64_t sum_simple(uint64_t *vec, size_t vecsize)
{
    uint64_t res = 0;
    size_t i;

    for (i = 0; i < vecsize; i++) {
        res += vec[i];
    }

    return res;
}

static uint64_t arr[BUFSIZE];

int main(void)
{
	int i;
	uint64_t ret = 0;

	for (i = 0; i < LOOPS; i++) {
		ret += (int)sum_simple(arr, BUFSIZE);
	}

	return ret;
}
