
#ifndef _PACKET_H
#define _PACKET_H

struct packet {
    uint8_t data[100];
    uint16_t len;
    bool broadcast;
    uint64_t remote_addr64;
    uint16_t remote_addr16;
};

#endif  // _RADIO_H
