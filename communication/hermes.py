import sys
from communication.velocity import Velocity
from communication.message import Message
from communication.serialCommunication import SerialCommunication


class Hermes:

    def __init__(self, callback):
        self.callback = callback

        self.serialCom = SerialCommunication()
        self.messages = []

        print("Hermes summoned")

    def setup(self, port, baud=115200):
        self.startBee(port, baud)

    '''
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
    '''

    # TODO Retornar lista de strings com as mensagens enviadas
    def fly(self, velocities):        
        """Main class method
            
            Receive velocities and manipulate, invoking create,
            send and clear methods.

            Args:
                velocities (vector): All robot velocities

            Returns:

        """
        robots = [
            # robot 1
            [
                0,
                velocities[0]['vLeft'],
                velocities[0]['vRight']
            ],
            # robot 2
            [
                1,
                velocities[1]['vLeft'],
                velocities[1]['vRight']
            ],
            # robot 3
            [
                2,
                velocities[2]['vLeft'],
                velocities[2]['vRight']
            ],
        ]
        messages = self.createMessages(robots)

        self.sendMessages()
        self.clearMessages()
        self.callback(messages)
        return messages

    def startBee(self, port, baud):
        """ Start xBee connection

        Verifies if port is serial, invoking isSerial() and
        create a xbee connection with serialCommunication method
        startBee.
         Args:
            port (string): Computer serial port
            baud (int): transmission speed
         Returns: string containing sucess or failure
        """
        if self.isSerial(port):
            self.xbee = self.serialCom.startBee(port, baud)
            return "bee started!"
        else:
            return "bee was not started :("

    def killBee(self):
        """
        Close xBee connection
            
        Invokes killBee method from serialCommunication

            Args:

            Returns:

        """
        self.serialCom.killBee()

    def sendMessages(self):
        """
        Send messages

        Use messages vector and call sendMessage() method
         Args:
         Returns:
        """
        for message in self.messages:
            self.sendMessage(message.robotId, message.message)
    
    def sendMessage(self, robotId, message):
        """
        Create all messages

        Receives velocities vector and manipulate information creating messages
        for all robots using createMessage() method.
        method sendMessage
         Args:
             robotId (id): Robot id
             message (Message): Message object to be sent
         Returns:
        """
        return self.serialCom.sendMessage(robotId, message)

    def createMessages(self, velocities):    
        """
        Create a message

        Receives robotId, and both wheels velocity, creating a string and
        putting into messages vector.
        Args:
            velocities
        Returns: a string containing created message
        """
        messages = []
        for robot in velocities:
            messages.append(self.createMessage(robot[0], robot[1], robot[2]))
            # self.createMessage(robot.id, robot.left_wheel, robot.right_wheel)

        return messages

    def createMessage(self, robotId, left_wheel, right_wheel):
        """
        Create a message

        Receives robotId, and both wheels velocity, creating a string and
        putting into messages vector.
        Args:
            robotId (id): Robot id
            left_wheel (float): left wheel velocity
            right_wheel (float): right wheel velocity
        Returns: a string containing created message
        """
        message = str(left_wheel) + ";" + str(right_wheel)
        self.messages.append(Message(robotId, message))
        return message

    def clearMessages(self):    
        """Verifies if is Serial port

        Based on operation system, verifies if port is serial using ttyUSB or COM patterns

        Args:

        Returns: Boolean, true if is serial port
                          false if is not
        """
        self.messages = []

    def isSerial(self, port):
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
