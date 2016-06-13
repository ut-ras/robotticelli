
#ifndef _ENCODER_H
#define _ENCODER_H


#include <mbed.h>


class QuadEncoder {
protected:
    InterruptIn _out_a, _out_b;
    int8_t _state;
    bool _error;
    int32_t _count;

    void _enc_isr(void);

public:
    QuadEncoder(PinName a, PinName b);
    bool ticks(int32_t &);
};


#endif // _ENCODER_H
