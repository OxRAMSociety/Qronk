/*
QRONK 2024
Example program for writing position data to 12 ST3215 Servo Motors
Modified from Waveshare examples: https://www.waveshare.com/wiki/ST3215_Servo
*/

#include <SCServo.h>

SMS_STS st;

// the uart used to control servos.
// GPIO 18 - S_RXD, GPIO 19 - S_TXD, as default.
#define S_RXD 18
#define S_TXD 19

void setup()
{
  Serial.begin(115200);
  Serial1.begin(1000000, SERIAL_8N1, S_RXD, S_TXD);
  st.pSerial = &Serial1;
  delay(1000);
}

void loop()
{
  int sz = 12;
  u8 ids[sz];
  u16 spds[sz];
  u8 accs[sz];
  s16 poss1[sz];
  s16 poss2[sz];

  unsigned int i = 0;
  for (i = 0; i < sz; i++) {
    ids[i] = i+1;
    spds[i] = (i+1)*5000/sz;
    accs[i] = 50;
    poss1[i] = 4095;
    poss2[i] = 2000; 
  }

  st.SyncWritePosEx(ids, sz, poss1, spds, accs);//servo(ID1) speed=3400，acc=50，move to position=4095.
  delay(2000);

  float ave = 0;
  int count = 0;
  for (int i = 0; i<sz; i++){
    int temp = st.ReadTemper(i+1);
    if (temp != -1) {
      ave += temp;
      count ++;
    }
  }
  ave /=count;
  Serial.println(ave);

  st.SyncWritePosEx(ids, sz, poss2, spds, accs);//servo(ID1) speed=3400，acc=50，move to position=4095.
  delay(2000);
}