
#include <mbed.h>
#include <rtos.h>

#include <radio.h>


int main()
{
    radio_init();
    while (true) {
        packet pkt;
        if (radio_recv(pkt, osWaitForever)) {
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
    }
}
