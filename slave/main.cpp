#include <Arduino.h>
#include <XBee.h>

XBee xbee = XBee();
ZBTxRequest zbTx;

void setup() {
  Serial.begin(9600);
  xbee.setSerial(Serial);
  uint8_t payload[] = {'H','i'};
  XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x403e0f30);
  zbTx = ZBTxRequest(addr64, payload, sizeof(payload));

}

void loop() {
  Serial.println("alive");
  xbee.send(zbTx);
  delay(1000);
}
