#include <stdio.h>

extern int lzma_compress(const char *input, char *output, int output_size);

void systemd_use_liblzma(const char *input) {
    char output[100];
    int compressed_length = lzma_compress(input, output, sizeof(output));
    if (compressed_length < 0) {
        printf("Compression failed\n");
    } else {
        printf("Compressed output: ");
        for (int i = 0; i < compressed_length; ++i) {
            putchar(output[i]);
        }
        putchar('\n');
    }
}
