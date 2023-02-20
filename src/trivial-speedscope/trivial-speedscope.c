#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#define	LOOPS 1024
#define BUFSIZE 4096

void read_file(void)
{
	int buf[BUFSIZE];
	int fd = open("/dev/urandom", O_RDONLY);
	int loops = LOOPS;

	while (loops--) {
		read(fd, buf, BUFSIZE);
	}

	close(fd);
}

void read_urand1(void) { read_file(); }
void read_urand2(void) { read_file(); }


int main(void)
{
	while (1) {
		read_urand1();
		read_urand2();
	}

	return 0;
}
