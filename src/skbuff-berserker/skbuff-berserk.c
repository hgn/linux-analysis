#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define SERVER_PORT 12345
//#define SERVER_IP "::1"
#define SERVER_IP "2001:4860:4860::8888"
#define BUFFER_SIZE 500

static void send_udp_packets(const int sockfd, const char *server_ip, int
		server_port, unsigned tx_iterations)
{
	struct sockaddr_in6 server_addr;
	char buffer[BUFFER_SIZE];
	ssize_t sent_bytes;

	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin6_family = AF_INET6;
	server_addr.sin6_port = htons(server_port);
	if (inet_pton(AF_INET6, server_ip, &server_addr.sin6_addr) <= 0) {
		perror("Invalid address/ Address not supported");
		close(sockfd);
		exit(EXIT_FAILURE);
	}

	memset(buffer, 'A', BUFFER_SIZE);


	sent_bytes = sendto(sockfd, buffer, BUFFER_SIZE, 0,
			(struct sockaddr *)&server_addr, sizeof(server_addr));
	if (sent_bytes < 0) {
		perror("sendto failed");
		return;
	}

	sleep(1);
	while (tx_iterations--) {
		sent_bytes = sendto(sockfd, buffer, BUFFER_SIZE, 0,
				(struct sockaddr *)&server_addr, sizeof(server_addr));
		if (sent_bytes < 0) {
			perror("sendto failed");
			break;
		}
	}

}


int main(void)
{
	int sockfd;
	unsigned tx_iterations = 50000;

	sockfd = socket(AF_INET6, SOCK_DGRAM, 0);
	if (sockfd < 0) {
		perror("socket creation failed");
		exit(EXIT_FAILURE);
	}

	send_udp_packets(sockfd, SERVER_IP, SERVER_PORT, tx_iterations);

	close(sockfd);

	return 0;
}
