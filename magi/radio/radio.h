
#ifndef _RADIO_H
#define _RADIO_H


#include <mbed.h>
#include <rtos.h>
#include <XBeeLib.h>


struct packet {
    uint8_t data[100];
    uint16_t len;
    bool broadcast;
    uint64_t remote_addr64;
    uint16_t remote_addr16;
};

#ifndef RADIO_QUEUE_SIZE
#define RADIO_QUEUE_SIZE 16
#endif  // RADIO_QUEUE_SIZE

bool radio_init(uint32_t timeout=osWaitForever);
bool radio_send(packet const& pkt);
bool radio_bcast(packet const& pkt);
bool radio_send(packet const& pkt, const XBeeLib::RemoteXBeeZB& RemoteDevice);
bool radio_recv(packet& dst, uint32_t wait);

#endif  // _RADIO_H
