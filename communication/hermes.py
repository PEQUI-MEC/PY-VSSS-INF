import sys
from xbee import XBee
from serial import Serial, SerialException, SerialTimeoutException, serialutil


class Hermes:

    def __init__(self):
        self.xbee = None
        self.serial = None
        self.robots = {
            "A": "\x56\x0D",
            "B": "\x5B\x0D",
            "C": "\x45\x0D"
        }
        print("Hermes summoned")

    def setup(self, port, baud=115200):
        try:
            self.serial = Serial(port, baud, writeTimeout=0)
            self.xbee = XBee(self.serial)
            print("Hermes is set up")
            return True
        except SerialException:
            print("In Hermes set up: Error opening xBee connection")
            
        return False

    def fly(self, velocities):
        """Main class method
            
            Receive velocities and manipulate, invoking send method

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
                ]
            ]

            Args:
                velocities (vector): All robot velocities

            Returns:

        """

        messages = []
        for i in range(len(velocities)):
            message = "{:.2f}".format(velocities[i]["vRight"]) + ";" + "{:.2f}".format(velocities[i]["vLeft"])
            self.sendMessage(i, message)
            messages.append((i, message))
            
        return messages

    def killBee(self):
        """
        Close xBee connection
            
        Invokes killBee method from serialCommunication

            Args:

            Returns:

        """
        self.serial.close()

    def sendMessage(self, robotId, message):
        """
        Send a message
        
            Args:
                robotId: Robot id
                message: Message to be sent
            Returns:
                String containing message sent

        """
        if self.xbee is not None:
            try:
                self.xbee.send("tx", frame='A', command='MY', dest_addr=self.robots[velocities[i]["robotLetter"]], data=message)
                return message
            except SerialTimeoutException:
                print("[Hermes]: Message sending timed out")
            except KeyError:
                print("[Hermes]: We don't know the address for robot '" + velocities[i]["robotLetter"] + "'")
            except SerialException:
                print("[Hermes]: Access to xBee denied")

        return None

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
