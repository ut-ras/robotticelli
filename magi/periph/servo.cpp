
#include <mbed.h>

#include "servo.h"


template<typename T>
T clamp(T x, T left, T right)
{
    return (x < left ? left : (x > right ? right : x));
}


Servo::Servo(PinName pin, uint16_t range) : _pwm(pin)
{
    // 0.5 ms to 2.5 ms is the maximum rating for most servos.
    _range = clamp(range, (uint16_t) 0, (uint16_t) 2000);
    _pwm.period_ms(20);
    _pwm.write(0.0);
}

Servo& Servo::operator=(double val)
{
    this->write(val);
    return *this;
}

void Servo::write(double val)
{
    _pwm.pulsewidth_us(1500 + (_range * clamp(val, -0.5, 0.5)));
}

double Servo::read(void)
{
    double val = (double) _pwm.read();
    return ((val * 20000) - 1500) / _range;
}

Servo::operator double(void)
{
    return this->read();
}
