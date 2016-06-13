
#include <algorithm>

#include <mbed.h>
#include <rtos.h>

#include <radio.h>


int main()
{
    uint8_t speed = 0;
    DigitalIn sw2(SW2), sw3(SW3);
    PwmOut pwm(PTC3);

    pwm.write(speed * 0.05);

    radio_init();
    while (true) {
        packet pkt;
        if (radio_recv(pkt, 10)) {
            printf(
                    "\r\nGot a %s RX packet [%08lx:%08lx|%04x], "
                    "len %d\r\nData: ",
                    pkt.broadcast ? "BROADCAST" : "UNICAST",
                    uint32_t (pkt.remote_addr64 >> 32),
                    uint32_t (pkt.remote_addr64 & 0xFFFFFFFF),
                    pkt.remote_addr16,
                    pkt.len);
            printf("%.*s\r\n", pkt.len, pkt.data);

            radio_send(pkt);
        }

        if (sw2 == 0) {
            while (sw2 == 0);
            speed = min(speed + 1, 20);
            speed += 1;
            pwm.write(speed * 0.05);
        }

        if (sw3 == 0) {
            while (sw3 == 0);
            speed = max(speed - 1, 0);
            pwm.write(speed * 0.05);
        }

    }
}
