
#include <mbed.h>
#include <rtos.h>

#include "encoder.h"


static const int8_t enc_lookup[16] = {
     0, /* 00 -> 00 */ -1, /* 00 -> 01 */  1, /* 00 -> 10 */  2, /* 00 -> 11 */
     1, /* 01 -> 00 */  0, /* 01 -> 01 */  2, /* 01 -> 10 */ -1, /* 01 -> 11 */
    -1, /* 10 -> 00 */  2, /* 10 -> 01 */  0, /* 10 -> 10 */  1, /* 10 -> 11 */
     2, /* 11 -> 00 */  1, /* 11 -> 01 */ -1, /* 11 -> 10 */  0, /* 11 -> 11 */
};


bool QuadEncoder::ticks(int32_t& ret)
{
    bool err;

    __disable_irq();

    err = _error;
    ret = _count;
    _count = 0;

    __enable_irq();

    return err;
}

void QuadEncoder::_enc_isr(void)
{
    int8_t current = (_out_a << 1) | _out_b;
    current = current ^ (current >> 1);

    int8_t inc = enc_lookup[((_state << 2) | current) & 0xFF];
    if (inc == 2) {
        _error = true;
    } else {
        _count += inc;
    }

    _state = current;
}

QuadEncoder::QuadEncoder(PinName a, PinName b) :
    _out_a(a), _out_b(b), _state(0x00), _error(false)
{
    __disable_irq();

    _out_a.disable_irq();
    _out_b.disable_irq();

    _out_a.rise(this, &QuadEncoder::_enc_isr);
    _out_a.fall(this, &QuadEncoder::_enc_isr);
    _out_b.rise(this, &QuadEncoder::_enc_isr);
    _out_b.fall(this, &QuadEncoder::_enc_isr);

    _out_a.enable_irq();
    _out_b.enable_irq();

    __enable_irq();
}
