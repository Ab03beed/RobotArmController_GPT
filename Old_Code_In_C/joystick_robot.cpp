#include "robot.h"
#include "joystick.h"
#include <unistd.h>
#include <stdio.h>
#include <iostream>
using namespace std;

// Maximum speed
float s = 0.01;

int main(int argc, char** argv){
	Robot robot;
	JOINT j = robot.position;
    Joystick joystick("/dev/input/js0");

    if (!joystick.isFound()){
        printf("Could not find joystick.\n");
        exit(1);
    }
	
    float j1 = 0.0;
    float j2 = 0.0;
    float j3 = 0.0;
    float j4 = 0.0;

    bool j5p = false;
    bool j5n = false;
    bool j6p = false;
    bool j6n = false;

    while (true){
        usleep(10000);
        JoystickEvent event;
        if (joystick.sample(&event)){
            if (event.isButton()){
                switch(event.number){
                case 4:
                    j5p=event.value;
                    j5n=false;
                    break;
                case 5:
                    j6p=event.value;
                    j6n=false;
                    break;
                case 6:
                    j5n=event.value;
                    j5p=false;
                    break;
                case 7:
                    j6n=event.value;
                    j6p=false;
                    break;
                default:
                    break;
                }
            } else if (event.isAxis()){
                switch(event.number){
                case 0:
                    j1 = event.value / -32767.0f;
                    break;
                case 1:
                    j3 = event.value / 32767.0f;
                    break;
                case 2:
                    j2 = event.value / -32767.0f;
                    break;
                case 3:
                    j4 = event.value / 32767.0f;
                    break;
                default:
                    break;
                }
            }
        }

        j.j1 += s * j1;
        j.j2 += s * j2;
        j.j3 += s * j3;
        j.j4 += s * j4;

        j.j5 += s * j5p;
        j.j5 -= s * j5n;
        j.j6 += s * j6p;
        j.j6 -= s * j6n;
        robot.write(j);
    }
}