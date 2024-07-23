#include <cstdint>
#include <iostream>

struct Tweedle {
	uint64_t dee;
	uint64_t dum;
};

namespace wonderland
{
	uint64_t swap_dum(Tweedle* t, uint64_t new_dum)
	{
		uint64_t prev_dum = t->dum;
		t->dum = new_dum;
		return prev_dum;
	}
}

int main()
{
	uint64_t prev_dum;
	Tweedle t = { 0x1234, 0x5678 };

	prev_dum = wonderland::swap_dum(&t, 0x9abc);

	return static_cast<int>(prev_dum);
}

