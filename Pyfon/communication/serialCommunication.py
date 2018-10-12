import time
from communication.robot import Robot
from xbee import XBee
from serial import Serial

class SerialCommunication():

    """ Serial Communication constructor
        
        Initializes xbee and serial as none and receives robots vector from Robot class.

        Args:

        Returns:

    """
    def __init__(self):
        self.xbee = None
        self.serial = None
        self.robots = Robot().robots

    """ Start xbee connection
        
        Start xbee connect through serial.

        Args:
            port (string): Serial port
            baud (int): transmission speed

        Returns:

    """
    def startBee(self, port, baud):
        self.serial = Serial(port, baud)
        self.xbee = XBee(self.serial)

    """ Close xbee connection
        
        Kill xbee, closing the serial connection

        Args:

        Returns:

    """
    def killBee(self):
        self.serial.close()

    """ Send message
        
        Send a message, using xbee method xbee.send(), getting from robots vector the robot address
        and message received as parameter

        Args:
            robotId (int): Robot Id
            message (string): string to send

        Returns:

    """
    def sendMessage(self, robotId, message):
        self.xbee.send("tx", frame = 'A',command='MY',dest_addr=self.robots[robotId-1],data=message)

    """ Create a robot

        Args:
            letter (string): Robot identification
            address (string): Robot address

        Returns:

    """
    def newRobot(letter, address):
        return True