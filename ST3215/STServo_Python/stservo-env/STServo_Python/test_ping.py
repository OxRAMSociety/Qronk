from STservo_sdk import *
import time

DEVICENAME = '/dev/serial0'

baudrates = [
    115200,
    1000000,
    57600
]

for baud in baudrates:

    print("\n====================")
    print("Trying baud:", baud)

    portHandler = PortHandler(DEVICENAME)
    packetHandler = sts(portHandler)

    portHandler.openPort()
    portHandler.setBaudRate(baud)

    time.sleep(1)

    for sid in range(0, 20):

        model, comm, err = packetHandler.ping(sid)

        print(
            "baud:", baud,
            "id:", sid,
            packetHandler.getTxRxResult(comm),
            "err:", err
        )

        if comm == COMM_SUCCESS:
            print("FOUND SERVO")
            print("ID:", sid)
            print("MODEL:", model)

        time.sleep(0.2)

    portHandler.closePort()

    time.sleep(1)