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

	if((fd=socket(AF_INET, SOCK_DGRAM, 0))==-1) {
		exit(1); 
	}

	hostptr=gethostbyname("douro");

	memset((void*)&serveraddr, (int)'\0', sizeof(serveraddr));
	serveraddr.sin_family=AF_INET;
	serveraddr.sin_addr.s_addr=((struct in_addr *)(hostptr->h_addr_list[0]))->s_addr;
	serveraddr.sin_port=htons((u_short)PORT);

	char msg[20];
	strcpy(msg, "ola server\n");
	addrlen = sizeof(serveraddr);
	printf("antes ifs\n");
	//if((sendto(fd, msg, strlen(msg)+1, 0, (struct sockaddr*)&serveraddr, addrlen))==-1) { printf("exit\n"); exit(1); }
	sendto(fd, msg, strlen(msg)+1, 0, (struct sockaddr*)&serveraddr, addrlen);
	printf("client enviou\n");
	recvfrom(fd, buffer, sizeof(buffer), 0, (struct sockaddr*)&serveraddr, &addrlen);
	printf("client recebeu\n");
	printf("%s\n", buffer);

	close(fd);
	exit(0);

}

