
#include <mbed.h>
#include <rtos.h>

#include <XBeeLib.h>

#include <radio.h>
#include "servo.h"
#include "pin_map.h"

#define PAINT_NEUTRAL 0.5
#define PAINT_SPRAY -0.5
#define PAINT_TIME 0.7



Servo paint_heads[SERVO_COUNT] = {
    Servo(PTD2, 2000),
    Servo(PTD0, 2000),
    Servo(PTC4, 2000),
    Servo(PTA0, 2000),
};

int main()
{
    DigitalIn sw2(SW2);
    DigitalIn sw3(SW3);

    for (int i = 0; i < SERVO_COUNT; i++) {
        paint_heads[i] = PAINT_NEUTRAL;
    }

    radio_init(1500);

    const uint64_t remote_addr64 = UINT64(0x0013A200, 0x40d4f162);
    const XBeeLib::RemoteXBeeZB remoteDevice = XBeeLib::RemoteXBeeZB(
            remote_addr64);

    packet pkt;
    const char *data = "what's up man?";
    strncpy((char *) &pkt.data, data, 100);
    pkt.len = strlen(data);

    radio_send(pkt);
    radio_bcast(pkt);
    radio_send(pkt, remoteDevice);

    uint8_t current_head = 0;

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
            printf("painting\r\n");
            while (sw2 == 0);
            paint_heads[current_head % SERVO_COUNT] = PAINT_SPRAY;
            wait(PAINT_TIME);
            paint_heads[current_head % SERVO_COUNT] = PAINT_NEUTRAL;
        }

        if (sw3 == 0) {
            printf("head %d\r\n", current_head);
            current_head++;
            while (sw3 == 0);
        }
    }
}
