
#include <Gizwits.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <dht11.h>


Gizwits myGizwits;

const int DHT11PIN = 8;  //dht输入

dht11 DHT11;


void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

  myGizwits.begin();
}


void loop() {

  //Configure network

  unsigned long input1 = analogRead(A0);  //模拟引脚输入A0
  myGizwits.write(VALUE_Input1, input1);

  int chk = DHT11.read(DHT11PIN);
  switch (chk) {
    case DHTLIB_OK:

      long varW_temp = DHT11.temperature;  //Add Sensor Data Collection
      myGizwits.write(VALUE_temp, varW_temp);
      unsigned long varW_hum = DHT11.humidity;  //Add Sensor Data Collection
      myGizwits.write(VALUE_hum, varW_hum);

      break;
  }


  bool varR_Button = 0;
  if (myGizwits.hasBeenSet(EVENT_Button)) {
    myGizwits.read(EVENT_Button, &varR_Button);  //Address for storing data
  }


  myGizwits.process();
}