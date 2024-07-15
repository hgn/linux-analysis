#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <math.h>

static int perf_ctl_fd = -1;
static int perf_ack_fd = -1;

const char* enable_cmd = "enable";
const char* disable_cmd = "disable";
const char* ack_cmd = "ack\n";

static int send_command(const char* command)
{
	ssize_t ret;
	char ack[5];

	if (perf_ctl_fd == -1)
		return -EINVAL;
	if (perf_ack_fd == -1)
		return -EINVAL;

	ret = write(perf_ctl_fd, command, strlen(command));
	if (ret != (ssize_t)strlen(command))
		return -ENOBUFS;
	read(perf_ack_fd, ack, sizeof(ack));
	if (strcmp(ack, ack_cmd) != 0)
		return -ENOBUFS;

	return 0;
}

int perf_control_init(void)
{
	char* ctl_fd_env = secure_getenv("PERF_CTL_FD");
	char* ack_fd_env = secure_getenv("PERF_ACK_FD");

	if (ctl_fd_env && ack_fd_env) {
		perf_ctl_fd = atoi(ctl_fd_env);
		perf_ack_fd = atoi(ack_fd_env);
		return 0;
	}

	return -ENOBUFS;
}

void perf_control_fini(void)
{
	if (perf_ctl_fd != -1) {
		close(perf_ctl_fd);
		perf_ctl_fd = -1;
	}
	if (perf_ack_fd != -1) {
		close(perf_ack_fd);
		perf_ack_fd = -1;
	}
}


int perf_control_enable(void)
{
	return send_command(enable_cmd);
}

int perf_control_disable()
{
	return send_command(disable_cmd);
}

void dummy_work(int factor)
{
	const size_t num_iter = 30000000 * factor;
	volatile double result = 0;
	for (size_t i = 0; i < num_iter; ++i) {
		result += exp(1.1);
	}
}

void initialize() { dummy_work(5); }
void finalize() { dummy_work(8); }
void timestep() { dummy_work(3); }

void simulate()
{
	for (int i = 0; i < 10; ++i) {
		timestep();
	}
}

int main(int argc, char **argv)
{
	int ret;

	(void) argc;
	(void) argv;

	perf_control_init();

	initialize();

	fprintf(stderr, "try to enable perf ...\n");
	ret = perf_control_enable();
	if (ret != 0)
		fprintf(stderr, "..failed\n");
	simulate();
	fprintf(stderr, "try to disable perf ...\n");
	ret = perf_control_disable();
	if (ret != 0)
		fprintf(stderr, "..failed\n");

	finalize();
	return 0;
}
