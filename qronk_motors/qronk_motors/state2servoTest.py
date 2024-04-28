#2024

#Don't Run on a Raspberry Pi
#Only for testing on a computer

#Subscribe to the JointState message in ROS2 and pass it to a PCA9685 driver board, currently takes an
#angle and passes it on. Need to make an equivalent for angular velocity for continuous rotation servos.

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
#from qronk_interfaces.msg import JointVelocity
from math import pi

class JointSub(Node):

    def __init__(self,nServos):
        super().__init__('JointSub')
        
        # Subscribe to joint_states topic
        self.create_subscription(JointState,'joint_states',self.listener_callback,10)
        self.topic_freq = 30 # Hz
        self.max_speed = 50 # Angular vel
        
        # Initialize continuous servos
        self.servos = nServos*[0]

    def listener_callback(self, msg):
        # Unpack msg data
        _vels = msg.velocity # Angular [rpm]
        _speed_ratios = [vel / self.max_speed for vel in _vels]
        _pos = msg.position # Angles [rad]
        self.positionServo(_pos)

    def positionServo(self,pos):
        for i in range(len(self.servos)):
            p = pos[i]
            s = self.servos[i]
            if p > pi/2: #Maximum value of 180 deg - Need to tune this
                s = 180
            elif p < -pi/2: #Minimum of 0 deg - Need to tune this
                s = 0
            else:
                s = p*(180/pi)+90 #Set servo angle for all values inbetween
            self.servos[i] = s #TEST LINE
            print(self.servos) #TEST LINE
   
    def closeBus(self,servos): #Close the bus when finished
        pass

def main(args=None):
    n = 12 #Number of servos, Don't overload the board just yet!
    rclpy.init(args=args)
    minimal_subscriber = JointSub(n)
    try:
        rclpy.spin(minimal_subscriber)
    except KeyboardInterrupt:
        minimal_subscriber.closeBus(n)
        minimal_subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()