#include <stdint.h>
#include <inttypes.h>

struct tweedle {
	uint64_t dee;
	uint64_t dum;
};

uint64_t swap_dum(struct tweedle *t, uint64_t new_dum)
{
	uint64_t prev_dum = t->dum;
	t->dum = new_dum;
	return prev_dum;
}

int main(void)
{
	uint64_t prev_dum;
	struct tweedle t = {
		.dee = 0x1234,
		.dum = 0x5678
	};

	prev_dum = swap_dum(&t, 0x9abc);

	return (int)prev_dum;
}
