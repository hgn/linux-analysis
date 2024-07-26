#include <stdio.h>
#include "sdt.h"

int main(void)
{
	printf("main\n");
	STAP_PROBE(test, main);
	return 0;
}
