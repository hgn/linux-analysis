#include <math.h>

int main(void)
{
	unsigned iterations = 1e8;
	double val = 42.;
	do {
		val += sin(val);
		val += sin(val);
		val += sin(val);
		val += sin(val);
	} while (iterations--);
}
