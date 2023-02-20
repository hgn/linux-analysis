#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#if 1
# define _SDT_ASM_SECTION_AUTOGROUP_SUPPORT 0
# include <sdt-owned.h>
#else
# define STAP_PROBE(a, b)
# define STAP_PROBE1(a, b, c)
# define STAP_PROBE2(a, b, c, d)
#endif

void do_something(void)
{
	int i;

	for (i = 0; i < 1000000; i++)
		;
}

int read_packet(void)
{
	int packet = rand();
	STAP_PROBE1(static_probe_points, read_packet, packet);
	return packet;
}

void process_request(int packet)
{
	STAP_PROBE1(static_probe_points, process_request, packet);
	do_something();
}

int generate_reply(int packet)
{
	int reply_packet = rand();

	STAP_PROBE2(static_probe_points, generate_reply, packet, reply_packet);
	do_something();
	return reply_packet;
}

void transmit_reply(int reply_packet)
{
	STAP_PROBE1(static_probe_points, transmit_reply, reply_packet);
	do_something();
}

void packet_available(void)
{
	int packet, reply_packet;

	STAP_PROBE(static_probe_points, packet_available);
	packet = read_packet();
	process_request(packet);
	reply_packet = generate_reply(packet);
	transmit_reply(reply_packet);
}

int main(void) {
	int i = 10;

	while (i--) {
		packet_available();
		sleep(1);
	}
	return EXIT_SUCCESS;
}
