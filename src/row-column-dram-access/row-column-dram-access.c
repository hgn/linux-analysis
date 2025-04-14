#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <errno.h>

#define NUM_ROWS (1024 * 32)
#define NUM_COLS (1024 * 32)

static int **
allocate_matrix(size_t rows, size_t cols)
{
	int **matrix = NULL;
	size_t i;

	matrix = malloc(rows * sizeof(*matrix));
	if (!matrix) {
		errno = ENOMEM;
		goto err_out;
	}

	for (i = 0; i < rows; i++)
		matrix[i] = NULL;

	for (i = 0; i < rows; i++) {
		matrix[i] = malloc(cols * sizeof(**matrix));
		if (!matrix[i]) {
			errno = ENOMEM;
			goto err_free_rows;
		}
	}

	return matrix;

err_free_rows:
	fprintf(stderr, "Error: malloc failed for row %zu\n", i);
	while (i > 0) {
		i--;
		free(matrix[i]);
	}
	free(matrix);
err_out:
	perror("Error: allocate_matrix failed");
	exit(EXIT_FAILURE);
}

static void
free_matrix(int **matrix, size_t rows)
{
	size_t i;

	if (!matrix)
		return;

	for (i = 0; i < rows; i++)
		free(matrix[i]);
	free(matrix);
}

static void
iterate_col_row(int **matrix, size_t rows, size_t cols)
{
	size_t i, j;

	for (i = 0; i < rows; i++) {
		for (j = 0; j < cols; j++)
			matrix[j][i] = (int)i;
	}
}

static void
iterate_row_col(int **matrix, size_t rows, size_t cols)
{
	size_t i, j;

	for (i = 0; i < rows; i++) {
		for (j = 0; j < cols; j++)
			matrix[i][j] = (int)i;
	}
}

int
main(void)
{
	int **matrix;
	clock_t start_cpu, end_cpu;
	double time_col_row, time_row_col;

	matrix = allocate_matrix(NUM_ROWS, NUM_COLS);

	start_cpu = clock();
	iterate_col_row(matrix, NUM_ROWS, NUM_COLS);
	end_cpu = clock();
	time_col_row = ((double)(end_cpu - start_cpu)) / CLOCKS_PER_SEC;

	start_cpu = clock();
	iterate_row_col(matrix, NUM_ROWS, NUM_COLS);
	end_cpu = clock();
	time_row_col = ((double)(end_cpu - start_cpu)) / CLOCKS_PER_SEC;

	printf("Col-Major CPU time: %.4f s\n", time_col_row);
	printf("Row-Major CPU time: %.4f s\n", time_row_col);

	if (time_row_col > 0.00001) {
		printf("Row-Major factor: %.2fx faster\n",
		       time_col_row / time_row_col);
	} else {
		printf("Row-Major significantly faster (time near zero)\n");
	}

	free_matrix(matrix, NUM_ROWS);

	return EXIT_SUCCESS;
}
