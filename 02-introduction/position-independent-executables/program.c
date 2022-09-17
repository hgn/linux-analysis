#include <example.h>

#include <stdio.h>
#include <stdlib.h>

int main(void)
{
	fprintf(stderr, "main():     %p\n", main);
	fprintf(stderr, "function(): %p (offset to main: %p)\n", function, (void *)function - (void *)main);
	fprintf(stderr, "fprintf():  %p (offset to main: %p)\n", fprintf, (void *)fprintf - (void *)main);

	return 0;
}
