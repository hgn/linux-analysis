#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

void inner(void)
{
	int i;
	char *ptr;

	for (i = 0; i < 1000000; i++)
		;

	ptr = malloc(10);
	free(ptr);

	sleep(1);
}

void outer(int i)
{
	printf("outer: %d\n", i);
	inner();
}

int main(void) {
	int i = 10;

	while (i--) {
		outer(i);
	}
	return EXIT_SUCCESS;
}
