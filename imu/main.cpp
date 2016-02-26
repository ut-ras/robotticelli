/**
 * Copyright (c) 2015 Digi International Inc.,
 * All rights not expressly granted are reserved.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Digi International Inc. 11001 Bren Road East, Minnetonka, MN 55343
 * =======================================================================
 */

#include "mbed.h"
#include "XBeeLib.h"
#if defined(ENABLE_LOGGING)
#include "DigiLoggerMbedSerial.h"
using namespace DigiLog;
#endif

#define REMOTE_NODE_ADDR64_MSB  ((uint32_t)0x0013A200)

#define REMOTE_NODE_ADDR64_LSB  ((uint32_t)0x40d4f16f)

#define REMOTE_NODE_ADDR64      UINT64(REMOTE_NODE_ADDR64_MSB, REMOTE_NODE_ADDR64_LSB)

using namespace XBeeLib;

Serial *log_serial;

static void send_data_to_coordinator(XBeeZB& xbee)
{
    const char data[] = "send_data_to_coordinator";
    const uint16_t data_len = strlen(data);

    const TxStatus txStatus = xbee.send_data_to_coordinator((const uint8_t *)data, data_len);
    if (txStatus == TxStatusSuccess)
        log_serial->printf("send_data_to_coordinator OK\r\n");
    else
        log_serial->printf("send_data_to_coordinator failed with %d\r\n", (int) txStatus);
}

static void send_broadcast_data(XBeeZB& xbee)
{
    const char data[] = "send_broadcast_data";
    const uint16_t data_len = strlen(data);

    const TxStatus txStatus = xbee.send_data_broadcast((const uint8_t *)data, data_len);
    if (txStatus == TxStatusSuccess)
        log_serial->printf("send_broadcast_data OK\r\n");
    else
        log_serial->printf("send_broadcast_data failed with %d\r\n", (int) txStatus);
}

static void send_data_to_remote_node(XBeeZB& xbee, const RemoteXBeeZB& RemoteDevice)
{
    const char data[] = "send_data_to_remote_node";
    const uint16_t data_len = strlen(data);

    const TxStatus txStatus = xbee.send_data(RemoteDevice, (const uint8_t *)data, data_len);
    if (txStatus == TxStatusSuccess)
        log_serial->printf("send_data_to_remote_node OK\r\n");
    else
        log_serial->printf("send_data_to_remote_node failed with %d\r\n", (int) txStatus);
}

static void send_explicit_data_to_remote_node(XBeeZB& xbee, const RemoteXBeeZB& RemoteDevice)
{
    char data[] = "send_explicit_data_to_remote_node";
    const uint16_t data_len = strlen(data);
    const uint8_t dstEP = 0xE8;
    const uint8_t srcEP = 0xE8;
    const uint16_t clusterID = 0x0011;
    const uint16_t profileID = 0xC105;

    const TxStatus txStatus = xbee.send_data(RemoteDevice, dstEP, srcEP, clusterID, profileID, (const uint8_t *)data, data_len);
    if (txStatus == TxStatusSuccess)
        log_serial->printf("send_explicit_data_to_remote_node OK\r\n");
    else
        log_serial->printf("send_explicit_data_to_remote_node failed with %d\r\n", (int) txStatus);
}

int main()
{
    log_serial = new Serial(DEBUG_TX, DEBUG_RX);
    log_serial->baud(9600);
    log_serial->printf("Sample application to demo how to send unicast and broadcast data with the XBeeZB\r\n\r\n");
    log_serial->printf(XB_LIB_BANNER);

#if defined(ENABLE_LOGGING)
    new DigiLoggerMbedSerial(log_serial, LogLevelInfo);
#endif

    XBeeZB xbee = XBeeZB(RADIO_TX, RADIO_RX, RADIO_RESET, NC, NC, 9600);

    RadioStatus radioStatus = xbee.init();
    MBED_ASSERT(radioStatus == Success);

    /* Wait until the device has joined the network */
    log_serial->printf("Waiting for device to join the network: ");
    while (!xbee.is_joined()) {
        wait_ms(1000);
        log_serial->printf(".");
    }
    log_serial->printf("OK\r\n");

    const RemoteXBeeZB remoteDevice = RemoteXBeeZB(REMOTE_NODE_ADDR64);

    send_data_to_coordinator(xbee);
    send_broadcast_data(xbee);
    send_data_to_remote_node(xbee, remoteDevice);
    send_explicit_data_to_remote_node(xbee, remoteDevice);

    delete(log_serial);
}
