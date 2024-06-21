#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <unistd.h>

void print_maps(void)
{
    pid_t pid = getpid();
    char command[256];

    snprintf(command, sizeof(command), "cat /proc/%d/maps", pid);

    system(command);
}

int main()
{
	fprintf(stderr, "PID %d\n", getpid());

	print_maps();

	return 0;
}
