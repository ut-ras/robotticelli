#include "mbed/mbed.h"
#include "L3GD20.h"
#include "LSM303DLHC.h"
#include "config.h"


static float DELAY = 0.5;
L3GD20 gyro(I2C_SDA, I2C_SCL);
static DigitalOut led(LED3);
float g1;
float g2;
float g3;
Serial *log_serial;
LSM303DLHC magAccel(I2C_SDA, I2C_SCL);
float a1;
float a2;
float a3;
float m1;
float m2;
float m3;
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
        wait(DELAY);
        gyro.read(&g1, &g2, &g3);
        magAccel.read(&a1, &a2, &a3, &m1, &m2, &m3);
        log_serial->printf("gyro x: %.2f  y: %.2f  z: %.2f     ", g1, g2, g3);
        log_serial->printf("accel dx: %.2f dy: %.2f  dz: %.2f    ", a1, a2, a3);
        log_serial->printf("mag dx: %.2f  dy: %.2f  dz: %.2f\n\r", m1, m2, m3);
    }
}
