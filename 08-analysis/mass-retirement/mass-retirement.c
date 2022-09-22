#include <inttypes.h>
#include <signal.h>
#include <sys/types.h>
#include <unistd.h>



int main(int ac, char **av)
{
	//uint64_t a = ac, b = ac, c = ac, d = ac;
	uint64_t iterations = 10000000000;
	(void) av;
	while (iterations--) {
		asm("inc %r8");
		asm("inc %r9");
		asm("inc %r10");
		asm("inc %r11");
		asm("inc %r12");
		asm("inc %r13");
		asm("inc %r14");
		asm("inc %r15");
		//a++, b++, c++, d++;
	}
	//return (int)(a + b + c +d);
}
