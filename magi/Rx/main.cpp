#include <Arduino.h>
#include <XBee.h>

#define MAX_FRAME_DATA_SIZE 110



//XBee initialization code
XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();
ModemStatusResponse msr = ModemStatusResponse();

int LED = 51;

void ledStatus(){
    for (int i = 0; i<100; i++){
        digitalWrite(LED, HIGH);
        delay(10000);
        digitalWrite(LED, LOW);
    }    
}


void setup(){
    pinMode(LED, OUTPUT); 
    Serial.begin(9600);    
    xbee.begin(Serial);
}

void loop(){

    xbee.readPacket();

    if(xbee.getResponse().isAvailable()){
        //Received something
    }

    else if(xbee.getResponse().isError()){
        //Error reading packet
        digitalWrite(LED, HIGH);
    }


}
