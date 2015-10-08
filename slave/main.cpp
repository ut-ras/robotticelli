#include <Arduino.h>
#include <XBee.h>

XBee xbee = XBee();
XBeeResponse resp = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();
ModemStatusResponse msr = ModemStatusResponse();

int status_led = 13;
int error_led = 13;
int data_led = 13;

void setup() {
    Serial.begin(9600);
    xbee.begin(Serial);
    pinMode(status_led, OUTPUT);
    digitalWrite(status_led, LOW);
    delay(5000);


}

void loop() {
    char buffer[128];
    xbee.readPacket();

    digitalWrite(status_led, HIGH);

    resp = xbee.getResponse();
    if (resp.isAvailable()) {
        if (resp.getApiId() == ZB_RX_RESPONSE) {
            resp.getZBRxResponse(rx);

            if (rx.getOption() == ZB_PACKET_ACKNOWLEDGED) {
                // Sender got an ACK
            } else {
                // Sender did not get an ACK
            }

            digitalWrite(status_led, HIGH);

            snprintf(buffer, 128, "%.*s", rx.getData());
            Serial.print(buffer);
        } else if (resp.getApiId() == MODEM_STATUS_RESPONSE) {
            resp.getModemStatusResponse(msr);

            if (msr.getStatus() == ASSOCIATED) {
                // Associated to network
            } else if (msr.getStatus() == DISASSOCIATED) {
                // Disassocated from network
            } else {
                // Lolwut
            }
        } else {
            // Seriously, lolwut
        }
    } else if (resp.isError()){
        // Error
    }

    delay(100);
}
