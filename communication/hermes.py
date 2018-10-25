import sys
from xbee import XBee
from serial import Serial, SerialException, SerialTimeoutException


class Hermes:

    def __init__(self):
        self.xbee = None
        self.serial = None
        self.robots = [
            {
                "id": "C",
                "address": "\x56\x0D"
            },
            {
                "id": "F",
                "address": "\x6B\x0D"
            },
            {
                "id": "G",
                "address": "\x21\x5C"
            }
        ]

        print("Hermes summoned")

    def setup(self, port, baud=115200):
        try:
            self.serial = Serial(port, baud, writeTimeout=0)
            self.xbee = XBee(self.serial)
        except SerialException:
            print("Error opening xBee connection.")

        print("Hermes is set up")

    def fly(self, velocities):
        """Main class method
            
            Receive velocities and manipulate, invoking create,
            send and clear methods.

            #velocities should be received like:
            [
                #robot 1
                [
                    robot_id,
                    left_wheel_velocity,
                    right_wheel_velocity
                ],
                #robot 2
                [
                    robot_id,
                    left_wheel_velocity,
                    right wheel_velocity
                ],
                #robot 3
                [
                    robot_id
                    left_wheel_velocity
                    right_wheel_velocity
                ],
            ]

            Args:
                velocities (vector): All robot velocities

            Returns:

        """

        messages = []
        for i in range(len(velocities)):
            message = str(velocities[i]["vRight"]) + ";" + str(velocities[i]["vLeft"])

            if self.xbee is not None:
                try:
                    self.xbee.send("tx", frame='A', command='MY', dest_addr=self.robots[i]["address"], data=message)
                    messages.append(message)
                except SerialTimeoutException:
                    print("Message sending timed out")

        return messages

    def killBee(self):
        """
        Close xBee connection
            
        Invokes killBee method from serialCommunication

            Args:

            Returns:

        """
        self.serial.close()

    @staticmethod
    def isSerial(port):
        """Verifies if is Serial port
            
            Based on operation system, verifies if port is serial using ttyUSB or COM patterns
            
            Args:
            
            Returns: Boolean, true if is serial port
                              false if is not

        """
        if sys.platform.startswith('linux'):
            if 'ttyUSB' in port:
                return True
        elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            if 'COM' in port:   
                return True
        return False
