#include "mbed/mbed.h"
#include "L3GD20.h"
#include "config.h"

L3GD20 gyro(I2C_SDA, I2C_SCL);
static DigitalOut led(LED3);
float g1;
float g2;
float g3;
bool data = false;
Serial *log_serial;

/*static void blinky(void) {
    static DigitalOut led(LED1);
    static DigitalOut led2(LED2);
    static DigitalOut led3(LED3);
    static int i = 1;
    if (i%1==0) led = !led;
    if (i%2==0) led2 = !led2;
    if (i%4==0) led3 = !led3;
    i++;
//    printf("LED = %d%d%d \r\n",led.read(), led2.read(), led3.read());
}*/

int main(void) {
    log_serial = new Serial(DEBUG_TX, DEBUG_RX);
    log_serial->baud(9600);
  
    //    minar::Scheduler::postCallback(blinky).period(minar::milliseconds(50));
    //
    //
//    char cmd[2];
    while(true){
        led = !led;
   /*
     * figure out pyocd
     * get this to flash
     * figure out why read is not getting called
     */
        wait(0.5);
        data = gyro.read(&g1, &g2, &g3);
        if (data) log_serial->printf("x: %.2f  y: %.2f  z: %.2f\n\r", g1, g2, g3);
    }
}
