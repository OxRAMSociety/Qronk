#Modified from https://docs.circuitpython.org/projects/pca9685/en/latest/examples.html#servo-example
#2024

import time
from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50
n = 3
servos = n*[None]
for i in range(n):
    servos[i] = servo.Servo(pca.channels[i],min_pulse = 500, max_pulse = 2500,actuation_range = 180)
print("""Servo Homing: For Testing and Assembly. 
Input the angle from 0 to 180 which the servo needs to move to.
CTRL + C to exit""")

while True:
    angle = int(input("Angle (deg): "))
    for testServo in servos:
        testServo.angle = angle
        time.sleep(1)
