#define LOOP_LIMIT 500

void ying(void)
{
	unsigned i;

	for (i = 0; i <= LOOP_LIMIT; i++)
		;
}

void yang(void)
{
	unsigned i;

	for (i = 0; i <= LOOP_LIMIT; i++)
		;
}

void main(void) {
	unsigned i;

	for (i = 0; ;i++)
		i % 2 == 0 ? ying(): yang();
}

