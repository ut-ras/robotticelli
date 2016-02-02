#include <Arduino.h>
#include <XBee.h>

#define MAX_FRAME_DATA_SIZE 110

//XBee initialization code
XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();
ModemStatusResponse msr = ModemStatusResponse();

int LED = 51;
int L = 13;

void ledStatus(){
    for (int i = 0; i<100; i++){
        digitalWrite(LED, HIGH);
        delay(10000);
        digitalWrite(LED, LOW);
    }    
}


void setup(){
    pinMode(LED, OUTPUT);
    pinMode(L, OUTPUT);


    Serial1.begin(9600);
    Serial.begin(9600);    
    xbee.begin(Serial);
}

void loop(){

    Serial1.print("Hello\n");

    digitalWrite(L, HIGH);
    delay(1000);
    digitalWrite(L, LOW);

    xbee.readPacket();
    digitalWrite(L, LOW);

    if(xbee.getResponse().isAvailable()){
        //Received something
        Serial1.print("RECEIVED SOMETHING\n");
        digitalWrite(L, HIGH);
    }
    else if(xbee.getResponse().isError()){
        //Error reading packet
        Serial1.print("ERROR\n");
        digitalWrite(L, HIGH);
    }


}
