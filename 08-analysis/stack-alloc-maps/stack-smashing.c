#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define SMASH_INCREMENT 256
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

	do {
		smash(i);
		i += SMASH_INCREMENT; 
		if (i >= PEAK_WORK)
			break;
	} while (42);

}

