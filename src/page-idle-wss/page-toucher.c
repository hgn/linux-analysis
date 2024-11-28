#include <err.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>
#include <string.h>
#include <sys/mman.h> // For mmap() and madvise()

#define SZ_PAGE (4 * 1024)

#define ACCESS_ONCE(x) (*(volatile typeof(x) *)&(x))

char **pages;

int alloc_pages(int nr_pages)
{
    int i;

    pages = (char **)malloc(sizeof(char *) * nr_pages);
    if (!pages)
        err(1, "Failed to allocate memory for pages array");

    for (i = 0; i < nr_pages; i++) {
        // Allocate memory for each page using mmap
        pages[i] = mmap(NULL, SZ_PAGE, PROT_READ | PROT_WRITE,
                        MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        if (pages[i] == MAP_FAILED)
            err(1, "Failed to allocate page %d with mmap", i);

        if (madvise(pages[i], SZ_PAGE, MADV_NOHUGEPAGE) != 0) {
            perror("madvise");
            fprintf(stderr, "Warning: Unable to disable huge pages for page %d\n", i);
        }

        ACCESS_ONCE(pages[i][0]) = 1;
    }

    return 0;
}

int access_pages(int nr_pages)
{
    int i;

    for (i = 0; i < nr_pages; i++)
        ACCESS_ONCE(pages[i][0]) = 1;

    return 0;
}

void print_usage(const char *prog_name)
{
    printf("Usage: %s -n <number of pages> -a <number of pages to access> -s <sleeptime>\n", prog_name);
    printf("       --number <number of pages> --access <number of pages to access>\n");
}

int main(int argc, char *argv[])
{
    int nr_pages = -1;
    int nr_accesses = -1;
    int sleeptime = 1;
    int option;

    // Options parsing
    const struct option long_options[] = {
        {"number", required_argument, NULL, 'n'},
        {"access", required_argument, NULL, 'a'},
        {"sleep",  required_argument, NULL, 's'},
        {NULL, 0, NULL, 0}
    };

    while ((option = getopt_long(argc, argv, "n:a:s:", long_options, NULL)) != -1) {
        switch (option) {
        case 'n':
            nr_pages = atoi(optarg);
            if (nr_pages < 1)
                errx(1, "Invalid number of pages: %s", optarg);
            break;
        case 'a':
            nr_accesses = atoi(optarg);
            if (nr_accesses < 0)
                errx(1, "Invalid number of pages to access: %s", optarg);
            break;
        case 's':
            sleeptime = atoi(optarg);
            if (sleeptime < 0)
                errx(1, "Invalid sleeptime: %s", optarg);
            break;
        default:
            print_usage(argv[0]);
            return 1;
        }
    }

    if (nr_pages < 1 || nr_accesses < 0) {
        print_usage(argv[0]);
        return 1;
    }

    // Print PID
    printf("Application PID: %d\n", getpid());

    // Allocate pages and disable huge pages
    alloc_pages(nr_pages);

    while (1) {
	    printf("touching %d pages ...", nr_accesses);
	    access_pages(nr_accesses);
	    sleep(sleeptime);
    }

    return 0;
}

