import serial
import glob

ports = glob.glob('/dev/tty*')

for port in sorted(ports):

    try:
        print("\n====", port, "====")

        ser = serial.Serial(port, 115200, timeout=0.5)

        for _ in range(3):
            data = ser.readline()
            print(repr(data))

        ser.close()

    except:
        pass