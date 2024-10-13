#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void handle_alarm(int sig)
{
	(void) sig;
	_exit(0); 
}

int main(void)
{
	void *current_brk;
	void *new_brk;
	size_t page_size;

	signal(SIGALRM, handle_alarm);

	alarm(4);

	page_size = sysconf(_SC_PAGESIZE);
	current_brk = sbrk(0);

	while (1) {
		new_brk = (char*)current_brk + page_size;
		brk(new_brk);
		/* commend out to trigger on-demand memory allocation via page faults */
		*(char*)current_brk = 0;
		current_brk = new_brk;
	}

	return 0;
}

