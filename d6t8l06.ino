#include <Wire.h>

#define D6T_addr 0x0A // Address of OMRON D6T is 0x0A in hex
#define D6T_cmd 0x4C // Standard command is 4C in hex

int numbytes = 19; 
int numel = 8;
int rbuf[19];
int tdata[8]; // The data comming from the sensor is in 8 elements
float t_PTAT;

void setup()
{
  Wire.begin();
  Serial.begin(9600);

  pinMode(13, OUTPUT);
}
 
void loop()
{
  int i;
      // Step one - send commands to the sensor
      Wire.beginTransmission(D6T_addr);
      Wire.write(D6T_cmd);
      Wire.endTransmission();

      delay(70); // Delay between instruction and data acquisition

      // Read from the sensor
      // Need to send a read command here - but how will this work with 7 bit addressing?
      Wire.requestFrom(D6T_addr,numbytes); // D6T-8 returns 19 bytes 

      // Receive the data

      if (0 <= Wire.available()) { // If there is data still left in buffer
        i = 0; //?????
        for (i=0; i < numbytes; i++) {
          rbuf[i] = Wire.read();
        }
        t_PTAT = (rbuf[0] + (rbuf[1] << 8) ) * 0.1;
        for (i = 0; i < numel; i++) {
          tdata[i] = (rbuf[(i*2+2)] + (rbuf[(i*2+3)] << 8 )) * 0.1;
          Serial.print(tdata[i]);
          Serial.print(",");
        }
        Serial.print(t_PTAT);
        Serial.print("\r\n");
      }

  delay(100);          
}
