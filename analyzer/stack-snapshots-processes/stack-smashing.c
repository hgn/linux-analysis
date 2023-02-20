#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define SMASH_INCREMENT 128
#define PEAK_WORK (1024 * 1024)

static int cnt = 0;

static void smash(size_t smash_size)
{
	char pad[smash_size];

	memset(pad, 0, smash_size);

	char buf[32];
	sprintf(buf, "./parse-maps.py %u %zu %d", getpid(), smash_size, cnt);
	system(buf);
	cnt++;
}

int main(void)
{
	size_t i = 8;

	for (i = 0; i <= PEAK_WORK; i += SMASH_INCREMENT)
		smash(i);
}

