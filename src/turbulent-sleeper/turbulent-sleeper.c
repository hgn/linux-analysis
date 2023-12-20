#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <signal.h>
#include <sys/prctl.h>

#define NO_TIMERS 50000

static unsigned int dead_count = NO_TIMERS;


void new_me(const char *name)
{
	if (prctl(PR_SET_NAME, name, 0, 0, 0) == -1) {
		perror("prctl");
	}
}

void timer_handler(int signum) {
	(void) signum;
	if (!dead_count--)
		exit(EXIT_SUCCESS);
}


void second_half(void)
{
	struct sigevent sev;
	struct itimerspec its;
	struct sigaction sa;
	timer_t timerid;
	const char *comm = "sleeper-second";

	new_me(comm);

	sa.sa_handler = timer_handler;
	sa.sa_flags = 0;
	sigemptyset(&sa.sa_mask);
	sigaction(SIGALRM, &sa, NULL);

	sev.sigev_notify = SIGEV_SIGNAL;
	sev.sigev_signo = SIGALRM;
	sev.sigev_value.sival_ptr = &timerid;
	if (timer_create(CLOCK_REALTIME, &sev, &timerid) == -1) {
		perror("timer_create");
		exit(EXIT_FAILURE);
	}

	its.it_interval.tv_sec = 0;
	its.it_interval.tv_nsec = 1000000;
	its.it_value.tv_sec = 0;
	its.it_value.tv_nsec = 1000000;
	if (timer_settime(timerid, 0, &its, NULL) == -1) {
		perror("timer_settime");
		exit(EXIT_FAILURE);
	}

	// just sleep really long, if not the application
	// will exit here. The application is exited through
	// the signal handler
	while (1)
		sleep(1);
}

void first_half(void)
{
	struct timespec ts;
	unsigned int i = NO_TIMERS;
	const char *comm = "sleeper-first";

	new_me(comm);

	ts.tv_sec = 0;
	ts.tv_nsec = 1;

	while (i--) {
		nanosleep(&ts, NULL);
	}
}

int main(int ac, char **av)
{
	(void) ac; (void) av;

	first_half();
	second_half();
	return 0;
}
