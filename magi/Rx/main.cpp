/**
 * Copyright (c) 2009 Andrew Rapp. All rights reserved.
 *
 * This file is part of XBee-Arduino.
 *
 * XBee-Arduino is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * XBee-Arduino is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with XBee-Arduino.  If not, see <http://www.gnu.org/licenses/>.
 */
#include <stdio.h> 
#include <Arduino.h>
#include <XBee.h>

/*
This example is for Series 2 XBee
Receives a ZB RX packet and sets a PWM value based on packet data.
Error led is flashed if an unexpected packet is received
*/

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
// create reusable response objects for responses we expect to handle 
ZBRxResponse rx = ZBRxResponse();
ModemStatusResponse msr = ModemStatusResponse();

int statusLed = 10;
int errorLed = 11;
int dataLed = 12;

void flashLed(int pin, int times, int wait) {
    
    for (int i = 0; i < times; i++) {
      digitalWrite(pin, HIGH);
      delay(wait);
      digitalWrite(pin, LOW);
      
      if (i + 1 < times) {
        delay(wait);
      }
    }
}

void setup() {
  pinMode(statusLed, OUTPUT);
  pinMode(errorLed, OUTPUT);
  pinMode(dataLed,  OUTPUT);
  
  // start serial
  Serial.begin(9600);
  Serial1.begin(9600);
  xbee.begin(Serial);
  pinMode(19, INPUT);
  digitalWrite(19, HIGH);
  
  flashLed(statusLed, 3, 50);
}

// continuously reads packets, looking for ZB Receive or Modem Status
void loop() {
    Serial1.print(F("working\n"));
    xbee.readPacket();
    
    if (xbee.getResponse().isAvailable()) {
      // got something
      Serial1.print(F("got something\n"));
      
      if (xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
        // got a zb rx packet
	Serial1.print(F("got zb rx packet\n"));
        
        // now fill our zb rx class
        xbee.getResponse().getZBRxResponse(rx);
            
        if (rx.getOption() == ZB_PACKET_ACKNOWLEDGED) {
            // the sender got an ACK
		Serial1.print(F("acknowledged\n"));
            flashLed(statusLed, 10, 10);
        } else {
            // we got it (obviously) but sender didn't get an ACK
	    Serial1.print(F("not acknowledged\n"));
            flashLed(errorLed, 2, 20);
        }
        // set dataLed PWM to value of the first byte in the data
        analogWrite(dataLed, rx.getData(0));
      } else if (xbee.getResponse().getApiId() == MODEM_STATUS_RESPONSE) {
        xbee.getResponse().getModemStatusResponse(msr);
        // the local XBee sends this response on certain events, like association/dissociation
	Serial1.print(F("got modem status"));
        
        if (msr.getStatus() == ASSOCIATED) {
          // yay this is great.  flash led
	  Serial1.print(F("Is associated\n"));
          flashLed(statusLed, 10, 10);
        } else if (msr.getStatus() == DISASSOCIATED) {
          // this is awful.. flash led to show our discontent
          flashLed(errorLed, 10, 30);
	  Serial1.print(F("Not associated\n"));
        } else {
          // another status
          flashLed(statusLed, 5, 10);
	  Serial1.print(F("werid status\n"));
        }
      } else {
        // not something we were expecting
	Serial1.print(F("Unexpected data\n"));
        flashLed(errorLed, 1, 25);    
      }
    } else if (xbee.getResponse().isError()) {
      Serial1.print(F("Error reading packet.  Error code: \n"));  
      Serial1.print(xbee.getResponse().getErrorCode());
    }
      else{
	Serial1.print(F("Nothing is working :("));
	}
}
