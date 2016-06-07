
#include <algorithm>

#include <mbed.h>
#include <rtos.h>
#include <XBeeLib.h>

#include "radio.h"

using namespace XBeeLib;

XBeeZB *xbee;
Queue<packet, RADIO_QUEUE_SIZE> queue;

static void receive_cb(
        const RemoteXBeeZB& remote,
        bool broadcast,
        const uint8_t *const data,
        uint16_t len)
{
    packet *pkt = new packet();
    memcpy(pkt->data, data, max((uint16_t) 100, len));
    pkt->len = len;
    pkt->broadcast = broadcast;
    pkt->remote_addr64 = remote.get_addr64();
    pkt->remote_addr16 = remote.get_addr16();

    queue.put(pkt);
}

bool radio_send(packet const& pkt)
{
    return xbee->send_data_to_coordinator((const uint8_t *) pkt.data, pkt.len);
}

bool radio_bcast(packet const& pkt)
{
    return xbee->send_data_broadcast((const uint8_t *) pkt.data, pkt.len);
}

bool radio_send(packet const& pkt, const RemoteXBeeZB& RemoteDevice)
{
    return xbee->send_data(RemoteDevice, (const uint8_t *) pkt.data, pkt.len);
}

bool radio_init(uint32_t timeout)
{
    xbee = new XBeeZB(RADIO_TX, RADIO_RX, RADIO_RESET, NC, NC, 9600);

    xbee->register_receive_cb(&receive_cb);

    RadioStatus const radioStatus = xbee->init();
    MBED_ASSERT(radioStatus == Success);

    uint32_t delay = min(timeout, (uint32_t) 100);
    uint32_t count = 0;
    while (!xbee->is_joined()) {
        if (delay * count >= timeout && timeout != osWaitForever) {
            return false;
        }
        wait_ms(delay);
        count++;
    }

    return true;
}

void radio_deinit(void)
{
    delete(xbee);
}

bool radio_recv(packet& dst, uint32_t wait)
{
    osEvent evt = queue.get(wait);
    if (evt.status == osEventMessage) {
        packet *pkt = (packet *) evt.value.p;

        dst = *pkt;
        delete(pkt);
        return true;
    }

    return false;
}
