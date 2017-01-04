
#ifndef _SERVO_H
#define _SERVO_H


#include <mbed.h>


class Servo {
protected:
    PwmOut _pwm;
    uint16_t _range;

public:
    Servo(PinName pin, uint16_t range=1000);
    Servo& operator=(double val);
    void write(double val);
    double read(void);
    operator double(void);
};


#endif // _SERVO_H
