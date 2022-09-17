#include <stdlib.h>
#include <unistd.h>

int main(void) {
	write(STDOUT_FILENO, "Howdy World\n", 12);
	return EXIT_SUCCESS;
}
