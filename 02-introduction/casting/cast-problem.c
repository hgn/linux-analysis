#include <inttypes.h>

int usual_function(uint64_t argument)
{
	int32_t comparer = 2u;

	if (argument < comparer)
		return 1;
	return 0;
}
