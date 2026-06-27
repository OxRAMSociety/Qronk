import sys
import os
import time
import math

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

sys.path.append("..")
from STservo_sdk import *                   # Uses STServo SDK library

BAUDRATE                    = 1000000           # STServo default baudrate : 1000000
DEVICENAME                  = '/dev/ttyACM0'    # When RPi connected to HAT Bus Servo by USB-C

STS_MOVING_SPEED            = 2400          # SCServo moving speed
STS_MOVING_ACC              = 50            # SCServo moving acc

# Servo IDs for relevant limbs
SHOULDER_ID = 9
FLOAT_ID = 2

# If, when looking at a motor, a clockwise motion lowers the leg from neutral, then it has a direction of 1. Reverse case, -1.
SHOULDER_DIRECT = 1
FLOAT_DIRECT = -1

# Length of limbs
L0 = 60
L1 = 100

portHandler = PortHandler(DEVICENAME)
packetHandler = sts(portHandler)

def port_setup():
    global portHandler, packetHandler
    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()

# Convert a position in mm to a set of IK angles
def convert_position_angle(x,y):
    theta1 = math.acos((x**2 + y**2 - (L0**2 + L1**2))/(2*L0*L1))
    theta0 = math.atan2(y,x) - math.atan2(L1 * math.sin(theta1),(L0 + (L1*math.cos(theta1))))

    return (theta0, theta1)

# Converts an angle in radians into a motor angle
def rad_to_motor(value):
    return value*4095/(2*math.pi)

# Convert a set of IK angles into positions that the motors should turn to
def convert_angles_leg_motion(theta0, theta1, shoulder_direction, float_direction):
    ##TODO: validate that this position is within the range of motion achievable by the servo (r slightly less than l0 + l1)

    # Servo angle ranges from 0 to 4095, middle position is 2047
    shoulder_pos = int(2047 + (shoulder_direction * rad_to_motor(theta0)))
    float_pos = int(2047 + (float_direction * rad_to_motor(theta0 + theta1 - math.pi/2)))

    return (shoulder_pos, float_pos)

if __name__ == "__main__":
    port_setup()
    groupSyncRead = GroupSyncRead(packetHandler, STS_PRESENT_POSITION_L, 11)

    for count in range(6):
        # sts_addparam_result_shoulder = packetHandler.SyncWritePosEx(SHOULDER_ID, 2047 + count*100*SHOULDER_DIRECT, STS_MOVING_SPEED, STS_MOVING_ACC)
        # sts_addparam_result_float = packetHandler.SyncWritePosEx(FLOAT_ID,  2047 - count*100, STS_MOVING_SPEED, STS_MOVING_ACC)

        (th0, th1) = convert_position_angle(60 - (count*5), 100)
        (a0, a1) = convert_angles_leg_motion(th0, th1, SHOULDER_DIRECT, FLOAT_DIRECT)

        print("Shoulder pos: {}, Float pos: {}".format(a0, a1))

        sts_addparam_result_shoulder = packetHandler.SyncWritePosEx(SHOULDER_ID, a0, STS_MOVING_SPEED, STS_MOVING_ACC)
        sts_addparam_result_float = packetHandler.SyncWritePosEx(FLOAT_ID, a1, STS_MOVING_SPEED, STS_MOVING_ACC)

        sts_comm_result = packetHandler.groupSyncWrite.txPacket()

        # Clear syncwrite parameter storage
        packetHandler.groupSyncWrite.clearParam()
        time.sleep(0.002) #wait for servo status moving=1

        while 1:
            sts_addparam_result_shoulder = groupSyncRead.addParam(SHOULDER_ID)
            sts_addparam_result_float = groupSyncRead.addParam(FLOAT_ID)

            sts_comm_result = groupSyncRead.txRxPacket()

            sts_last_moving = 0

            for sts_id in (SHOULDER_ID, FLOAT_ID):
                sts_data_result, sts_error = groupSyncRead.isAvailable(sts_id, STS_PRESENT_POSITION_L, 11)

                if sts_data_result == True and groupSyncRead.getData(sts_id, STS_MOVING, 1) == 1:
                    sts_last_moving = 1

            groupSyncRead.clearParam()
            if sts_last_moving==0:
                time.sleep(1)
                break
                

    # Close port
    portHandler.closePort()