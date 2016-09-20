#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <netdb.h>
#include <stdlib.h>
#include <stdio.h>
#define PORT 59000

int main() {

	int fd;
	struct hostent *hostptr;
	struct sockaddr_in serveraddr, clientaddr;
	int addrlen;

	char buffer[128];
	printf("antes socket\n");
	fd=socket(AF_INET, SOCK_DGRAM, 0);
	if(fd == -1) {
		//This shouldn't happen
		exit(-1);
	}

	printf("antes memset\n");
	memset((void*)&serveraddr, (int)'\0', sizeof(serveraddr));

	serveraddr.sin_family=AF_INET;
	serveraddr.sin_addr.s_addr=htonl(INADDR_ANY);
	serveraddr.sin_port=htons((u_short)PORT);

	printf("antes bind\n");
	int bindTest = bind(fd, (struct sockaddr*)&serveraddr, sizeof(serveraddr));
	if(bindTest == -1) {
		//This shouldn't happen
		exit(-1);
	}	
	char msg[11] = "ola cliente";
	printf("antes while\n");

	while(1) {
		addrlen = sizeof(clientaddr);
		printf("antes receber server");
		recvfrom(fd, buffer, sizeof(buffer), 0, (struct sockaddr*)&clientaddr, &addrlen);
		printf("servidor recebeu\n");
		sendto(fd, msg, strlen(msg)+1, 0, (struct sockaddr*)&clientaddr, addrlen);
		printf("servidor enviou\n");
	}
	close(fd);
	exit(0);

}
