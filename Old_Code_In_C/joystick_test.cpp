#include "joystick.h"
#include <unistd.h>

int main(int argc, char** argv){
  Joystick joystick("/dev/input/js0");

  if (!joystick.isFound()){
    printf("open failed.\n");
    exit(1);
  }

  while (true){
    usleep(1000);

    JoystickEvent event;
    if (joystick.sample(&event))    {
      if (event.isButton()){
        printf("Button %u is %s\n",
          event.number,
          event.value == 0 ? "up" : "down");
      }
      else if (event.isAxis()){
        printf("Axis %u is at position %d\n", event.number, event.value);
      }
    }
  }
}