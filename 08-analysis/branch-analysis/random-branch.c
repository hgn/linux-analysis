#include <stdio.h>
#include <stdlib.h>


void aa(void)
{
	int i = 1000;
	while (i--)
		;
}

void ab(void)
{
	int i = 1000;
	while (i--)
		;
}

void ba(void)
{
	int i = 1000;
	while (i--)
		;
}

void bb(void)
{
	int i = 1000;
	while (i--)
		;
}


int a(void)
{
	if ((rand() % 2) == 0)
		aa();
	else
		ab();
}


int b(void)
{
	if ((rand() % 2) == 0)
		ba();
	else
		bb();
}



int main(void)
{
	int outer_loop_no = 1000000;

	while (outer_loop_no--) {
		if ((rand() % 2) == 0)
			a();
		else
			b();

	}

	return 0;
}
