
#include <mbed.h>
#include <rtos.h>

#include <XBeeLib.h>
#include <Servo.h>
#include <radio.h>

#include "pin_map.h"

using namespace XBeeLib;

#define PAINT_NEUTRAL 0.85
#define PAINT_SPRAY 1.0
#define PAINT_RANGE 0.0008
#define PAINT_TIME 0.2


Servo paint_heads[SERVO_COUNT] = {
    Servo(PTD2),
    Servo(PTD0),
    Servo(PTC4),
    Servo(PTA0),
};

int main()
{
    DigitalIn sw2(SW2);
    DigitalIn sw3(SW3);
    PwmOut pwm(PTC3);
    pwm.write(.1);

    for (int i = 0; i < SERVO_COUNT; i++) {
        paint_heads[i].calibrate(PAINT_RANGE);
        paint_heads[i].write(PAINT_NEUTRAL);
    }

    radio_init();

    const uint64_t remote_addr64 = UINT64(0x0013A200, 0x40d4f162);
    const RemoteXBeeZB remoteDevice = RemoteXBeeZB(remote_addr64);

    packet pkt;
    const char *data = "what's up man?";
    strncpy((char *) &pkt.data, data, 100);
    pkt.len = strlen(data);

    radio_send(pkt);
    radio_bcast(pkt);
    radio_send(pkt, remoteDevice);

    int current_head = 0;
    int toggle = 0;

    while (true) {
        packet pkt;
        if (radio_recv(pkt, 0)) {
            printf(
                    "\r\nGot a %s RX packet [%08lx:%08lx|%04x], "
                    "len %d\r\nData: ",
                    pkt.broadcast ? "BROADCAST" : "UNICAST",
                    uint32_t (pkt.remote_addr64 >> 32),
                    uint32_t (pkt.remote_addr64 & 0xFFFFFFFF),
                    pkt.remote_addr16,
                    pkt.len);
            printf("%.*s\r\n", pkt.len, pkt.data);
        }

        if (sw2 == 0) {
            printf("painting\n");
            while (sw2 == 0);
            paint_heads[current_head % SERVO_COUNT].write(PAINT_SPRAY);
            wait(PAINT_TIME);
            paint_heads[current_head % SERVO_COUNT].write(PAINT_NEUTRAL);
            toggle = !toggle;
            pwm.write(toggle ? 0.15 : 0.1);
        }

        if (sw3 == 0) {
            printf("head %d\n", current_head);
            current_head++;
            while (sw3 == 0);
            toggle = !toggle;
            pwm.write(toggle ? 0.15 : 0.1);
        }
    }
}
