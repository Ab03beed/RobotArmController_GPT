#ifndef __JOYSTICK_HH__
#define __JOYSTICK_HH__

#include <string>
#include <iostream>

#define JS_EVENT_BUTTON 0x01 // button pressed/released
#define JS_EVENT_AXIS   0x02 // joystick moved
#define JS_EVENT_INIT   0x80 // initial state of device

class JoystickEvent{
public:
  static const short MIN_AXES_VALUE = -32768;
  static const short MAX_AXES_VALUE = 32767;

  unsigned int time;
  short value;
  unsigned char type;
  unsigned char number;
  
  bool isButton(){
    return (type & JS_EVENT_BUTTON) != 0;
  }

  bool isAxis(){
    return (type & JS_EVENT_AXIS) != 0;
  }

  bool isInitialState(){
    return (type & JS_EVENT_INIT) != 0;
  }

  friend std::ostream& operator<<(std::ostream& os, const JoystickEvent& e);
};

std::ostream& operator<<(std::ostream& os, const JoystickEvent& e);

class Joystick{
private:
  void openPath(std::string devicePath, bool blocking=false);
  
  int _fd;
  
public:
  ~Joystick();
  Joystick();
  Joystick(int joystickNumber);
  Joystick(std::string devicePath);
  Joystick(Joystick const&) = delete;
  Joystick(Joystick &&) = default;
  Joystick(std::string devicePath, bool blocking);

  bool isFound();
  bool sample(JoystickEvent* event);
};

#endif