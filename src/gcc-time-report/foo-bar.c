#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <getopt.h>
#include <math.h>
#include <regex.h>

// Function to be executed by threads
void *thread_function(void *arg) {
    int *thread_id = (int *)arg;
    
    // Math operations
    double square_root_result = sqrt(*thread_id);
    double sine_result = sin(*thread_id);

    printf("Thread %d is running\n", *thread_id);
    printf("Square root of %d: %f\n", *thread_id, square_root_result);
    printf("Sine of %d: %f\n", *thread_id, sine_result);

    return NULL;
}

int main(int argc, char *argv[]) {
    int num_threads = 2;
    int option;

    // Parse command-line arguments using getopt and validate with regex
    regex_t regex;
    char regex_pattern[] = "^[0-9]+$";
    if (regcomp(&regex, regex_pattern, REG_EXTENDED) != 0) {
        fprintf(stderr, "Error compiling regex pattern\n");
        exit(EXIT_FAILURE);
    }

    while ((option = getopt(argc, argv, "n:")) != -1) {
        switch (option) {
            case 'n':
                if (regexec(&regex, optarg, 0, NULL, 0) != 0) {
                    fprintf(stderr, "Invalid argument for -n. Must be a positive integer.\n");
                    exit(EXIT_FAILURE);
                }
                num_threads = atoi(optarg);
                break;
            default:
                fprintf(stderr, "Usage: %s [-n num_threads]\n", argv[0]);
                exit(EXIT_FAILURE);
        }
    }

    // Validate the number of threads
    if (num_threads <= 0) {
        fprintf(stderr, "Number of threads must be greater than 0\n");
        exit(EXIT_FAILURE);
    }

    // Create an array to store thread IDs
    pthread_t threads[num_threads];
    int thread_ids[num_threads];

    // Spawn threads
    for (int i = 0; i < num_threads; ++i) {
        thread_ids[i] = i + 1; // Start thread IDs from 1
        if (pthread_create(&threads[i], NULL, thread_function, (void *)&thread_ids[i]) != 0) {
            fprintf(stderr, "Error creating thread %d\n", i);
            exit(EXIT_FAILURE);
        }
    }

    // Wait for threads to finish
    for (int i = 0; i < num_threads; ++i) {
        if (pthread_join(threads[i], NULL) != 0) {
            fprintf(stderr, "Error joining thread %d\n", i);
            exit(EXIT_FAILURE);
        }
    }

    printf("All threads have finished\n");

    // Free the regex resources
    regfree(&regex);

    return 0;
}
