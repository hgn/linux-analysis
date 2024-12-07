#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

#define BUF_SIZE 1

void read_file(const char *filename)
{
	int fd;
	char buffer[BUF_SIZE];
	ssize_t bytes_read;

	printf("Opening file: %s\n", filename);

	usleep(100000);

	/* Open the file */
	fd = open(filename, O_RDONLY);
	if (fd == -1) {
		perror("Error opening file");
		exit(EXIT_FAILURE);
	}

	/* Wait 1 second before reading */
	sleep(1);

	/* Read the file content and discard it */
	bytes_read = read(fd, buffer, BUF_SIZE);
	if (bytes_read == -1) {
		perror("Error reading file");
	}

	/* Wait 1 second before closing */
	sleep(1);

	/* Close the file */
	close(fd);
}

int main(int argc, char *argv[])
{
	if (argc != 2) {
		fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
		return EXIT_FAILURE;
	}

	read_file(argv[1]);
	return EXIT_SUCCESS;
}

