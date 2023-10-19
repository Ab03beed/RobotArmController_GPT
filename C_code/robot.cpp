#include "robot.h"
#include <iostream>
#include <cstring>
using namespace std;

Robot::Robot(){
	period_ = 0.0071;
	counter_ = 0;
	// initialize UDP socket
	socket_ = socket (AF_INET, SOCK_DGRAM, 0);
	if (socket_ < 0){
    	cout<<"Cannot open socket.";
    	exit(1);
    }
    // set IP and port
    ip = "192.168.0.20";
    port = 10000;
    addr_.sin_family = AF_INET;
    addr_.sin_port = htons (port);
  	addr_.sin_addr.s_addr = inet_addr (ip.c_str());

  	memset (&send_buff_, 0, sizeof (send_buff_));
  	memset (&recv_buff_, 0, sizeof (recv_buff_));

  	write_first();	
  	write_first();
}

void Robot::write_first(){
	memset (&send_buff_, 0, sizeof (send_buff_));
	send_buff_.Command = MXT_CMD_NULL;
	send_buff_.SendType = MXT_TYP_NULL;
	send_buff_.RecvType = MXT_TYP_JOINT;
	send_buff_.SendIOType = MXT_IO_NULL;
	send_buff_.RecvIOType = MXT_IO_NULL;
	send_buff_.BitTop = 0;
	send_buff_.BitMask = 0;
	send_buff_.IoData = 0;
	send_buff_.CCount = 0;

	int size = sendto (socket_, (char *) &send_buff_, sizeof (send_buff_), 0, (struct sockaddr *) &addr_, sizeof (addr_));
	if (size != sizeof (send_buff_)){
		cout<<"Cannot send packet to robot controller. Check the configuration.";
	    exit (1);
	}
	read();
}

void Robot::write(JOINT j){
	// Send MOVE command
	memset (&send_buff_, 0, sizeof (send_buff_));
	send_buff_.Command = MXT_CMD_MOVE;
	send_buff_.SendType = MXT_TYP_JOINT;
	send_buff_.RecvType = MXT_TYP_JOINT;
	send_buff_.RecvType1 = MXT_TYP_FJOINT;
	send_buff_.RecvType2 = MXT_TYP_FB_JOINT;
	send_buff_.RecvType3 = MXT_TYP_FBKCUR;

	send_buff_.SendIOType = MXT_IO_NULL;
	send_buff_.RecvIOType = MXT_IO_NULL;
	send_buff_.BitTop = 0;
	send_buff_.BitMask = 0;
	send_buff_.IoData = 0;
	send_buff_.dat.jnt.j1 = j.j1;
	send_buff_.dat.jnt.j2 = j.j2;
	send_buff_.dat.jnt.j3 = j.j3;
	send_buff_.dat.jnt.j4 = j.j4;
	send_buff_.dat.jnt.j5 = j.j5;
	send_buff_.dat.jnt.j6 = j.j6;
	send_buff_.CCount = counter_;

	int size = sendto (socket_, (char *) &send_buff_, sizeof (send_buff_), 0, (struct sockaddr *) &addr_, sizeof (addr_));
	if (size != sizeof (send_buff_)){
		cout<<"Cannot send packet to robot controller. Check the configuration.";
    	exit (1);
  	}
}

void Robot::read(){
	int size = recvfrom (socket_, &recv_buff_, sizeof (recv_buff_), 0, NULL, NULL);
	if (size < 0){
		cout<<"recvfrom failed";
		exit (1);
	}
	JOINT *joint = (JOINT *) & recv_buff_.dat;
	position.j1 = joint->j1;
	position.j2 = joint->j2;
	position.j3 = joint->j3;
	position.j4 = joint->j4;
	position.j5 = joint->j5;
	position.j6 = joint->j6;

    counter_++;
}