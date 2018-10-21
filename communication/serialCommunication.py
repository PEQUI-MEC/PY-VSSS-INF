import time
from communication.robot import Robot
from xbee import XBee
from serial import Serial


class SerialCommunication:

    def __init__(self):
        """ Serial Communication constructor
            
            Initializes xbee and serial as none and receives robots vector from Robot class.

            Args:

            Returns:

        """
        self.xbee = None
        self.serial = None
        self.robots = Robot().robots

    def startBee(self, port, baud):
        """ Start xbee connection
            
            Start xbee connect through serial.

            Args:
                port (string): Serial port
                baud (int): transmission speed

            Returns:

        """
        self.serial = Serial(port, baud)
        self.xbee = XBee(self.serial)
    
    def killBee(self):
        """ Close xbee connection
            
            Kill xbee, closing the serial connection

            Args:

            Returns:

        """
        self.serial.close()

    def sendMessage(self, robotId, message):
        """ Send message
            
            Send a message, using xbee method xbee.send(), getting from robots vector the robot address
            and message received as parameter

            Args:
                robotId (int): Robot Id
                message (string): string to send

            Returns:

        """
        self.xbee.send("tx", frame='A', command='MY', dest_addr=self.robots[robotId-1], data=message)
    
    def newRobot(self, letter, address):
        """ Create a robot

            Args:
                letter (string): Robot identification
                address (string): Robot address

            Returns:

        """
        return True
