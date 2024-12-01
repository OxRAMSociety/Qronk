/*
QRONK 2024
Example program for writing position data to 12 ST3215 Servo Motors
Prints average the current and temperature
Modified from Waveshare examples: https://www.waveshare.com/wiki/ST3215_Servo
*/

#include <SCServo.h>

SMS_STS st;

// the uart used to control servos.
// GPIO 18 - S_RXD, GPIO 19 - S_TXD, as default.
#define S_RXD 18
#define S_TXD 19

int cycles = 1;

void setup()
{
  //Initialise the serial ports used for communication with the servos and computer
  Serial.begin(115200);
  Serial1.begin(1000000, SERIAL_8N1, S_RXD, S_TXD);
  st.pSerial = &Serial1;
  delay(1000);
}

void loop()
{
  //Define arrays for position data
  int sz = 12;
  u8 ids[sz];
  u16 spds[sz];
  u8 accs[sz];
  s16 pos[sz];
  for (int i = 0; i < sz; i++) {
    ids[i] = i+1;
    spds[i] = 4000;
    accs[i] = 50;
    if (cycles %2 == 0){
      pos[i] = 0;
    }
    else{
      pos[i] = 4095;
    }
  } 
  //Send position commands to the servos
  st.SyncWritePosEx(ids, sz, pos, spds, accs);
  delay(2000);

  //Calculate the mean temperature and current for the motors
  float aveT = 0;
  float aveI = 0;
  int count = 0;
  for (int i = 0; i<sz; i++){
    int temp = st.ReadTemper(i+1);
    if (temp != -1) {
      aveT += temp;
      aveI += st.ReadCurrent(i+1);
      count ++;
    }
  }
  aveT /= count;
  aveI /= count;

  //Print the temps and currents to serial
  Serial.print("Temperature(C):");
  Serial.print(aveT);
  Serial.print(",");
  Serial.print("Current(A):");
  Serial.println(aveI);

  cycles ++;
}