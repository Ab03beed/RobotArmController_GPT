#include "strdef.h"
#include <string>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
using namespace std;

class Robot{
public: 
	Robot();
	void write(JOINT j);
	void read();

  	JOINT position;

private:
	void write_first();
	string ip;
	int port;
	int socket_;
	struct sockaddr_in addr_;

	MXTCMD send_buff_;
  	MXTCMD recv_buff_;
  	int counter_;
  	double period_;
};