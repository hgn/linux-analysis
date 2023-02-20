#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

static void function_three(void)
{
	abort();
}


static void function_two(void)
{
	function_three();
}

static void function_one(void)
{
	function_two();
}

int main(void)
{
	function_one();

	return EXIT_SUCCESS;
}
