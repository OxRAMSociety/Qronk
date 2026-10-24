import serial
import time

ser = serial.Serial('/dev/serial0', 115200, timeout=0.2)

while True:
    ser.write(b'\xFF\xFF\x01\x02\x01\xFB')
    time.sleep(0.1)

    data = ser.read(100)

    print(data)