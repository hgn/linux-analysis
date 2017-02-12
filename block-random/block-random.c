#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>


#define	LOOPS 1000

int main(void)
{
	int buf[1000000];
	int fd = open("/dev/urandom", O_RDONLY);
	int loops = LOOPS;

	while (loops--) {
		read(fd, buf, 1000000);
	}

	return 0;
}
