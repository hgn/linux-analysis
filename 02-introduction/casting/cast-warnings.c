#include <inttypes.h>

void func(char argument)
{
	(void) argument;
}

int main(void)
{
	const char a = 'x';

	func(a);

	return 0;
}
