#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped, PointStamped, Twist
import pprint

from helpers.endless import Endless
from strategy import Athena
from control import Zeus


class RosComm:
    def __init__(self, node_name, pub_freq=60, robot_index_start=0, n_robots=3, field_width=640, field_height=480, default_velocity=0.8):
        """
        Subscriber thread:
        - Receive observations
        - Process observations and holds an action

        Publisher thread: 
        - Publishes held actions and waits according to rate.
        """
        self.obs = []
        self.action = []
        self.pub_freq = pub_freq
        self.n_robots = n_robots
        self.robot_index_start = robot_index_start
        self.sync_integer = n_robots + 1  # integer to sync received positions + ball (can sync inconsistently but it's not a big deal)

        self.raw_positions = [PoseStamped() for i in range(n_robots)]
        self.raw_ball_position = 0

        self.positions = [False for i in range(n_robots)]
        self.actions = [Twist() for i in range(n_robots)]

        # VSSS controllers
        Endless.setup(field_width, field_height)
        self.athena = Athena()
        self.zeus = Zeus()
        self.athena.setup(n_robots, default_velocity)
        self.zeus.setup(n_robots)

        # ROS configs
        rospy.init_node(node_name, anonymous=True)

        ball_subscriber = rospy.Subscriber("ball", PointStamped, self.storeRawBallPosition)
        self.subscribers = [
            rospy.Subscriber("robot%d/pose" % i, PoseStamped, self.storeRawPosition, (i)) for i in range(robot_index_start, robot_index_start + n_robots)
        ]
        self.publishers = [
            rospy.Publisher("robot%d/cmd_vel" % i, Twist, queue_size=10) for i in range(robot_index_start, robot_index_start + n_robots)
        ]

        self.publisher()

    def publisher(self):
        rate = rospy.Rate(self.pub_freq)
        while not rospy.is_shutdown():
            for i in range(len(self.publishers)):
                action = self.actions[i]
                self.publishers[i].publish(action)
                # print("CONTROLLER PUBLISHED: " + str(action))

            rate.sleep()

    def generatePositions(self):
        """
        Converts simulator positions to be used by Athena and call the action generation.
        Args:
            obs: simulator observation
        Returns:
            List of cartesian coordinates
        """
        self.positions = [
            [ # robôs aliados
                {
                    "position": (raw_position.pose.position.x, raw_position.pose.position.y),
                    "orientation": raw_position.pose.position.z,
                    "robotLetter": 'A'
                } for raw_position in self.raw_positions
            ],
            [ # robôs adversários (TODO adicionar suporte a posição de adversários)
                {
                    "position": (0, 0)
                } for i in range(self.n_robots)
            ],
            { # bola
                "position": (self.raw_ball_position.pose.position.x, self.raw_ball_position.pose.position.y) if self.raw_ball_position is not 0 else (0, 0)
            }
        ]
        
        self.generateAction()


    def generateAction(self):
        """
        Gets converted simulator observations and uses VSSS controllers to 
        generate and store actions.
        """
        if(self.positions[0] == False):
            return

        commands = self.athena.getTargets(self.positions)
        velocities = self.zeus.getVelocities(commands)
        # convert wheel velocities to linear/angular velocities
        for i in range(self.n_robots):
            action = Twist()
            action.linear.x = (velocities[i]['vLeft'] + velocities[i]['vRight']) / 2
            action.angular.x = (velocities[i]['vLeft'] + velocities[i]['vRight']) / 2  # TODO consertar essas conversões
            self.actions[i] = action
        

    def storeRawPosition(self, data, index):
        index -= self.robot_index_start
        self.raw_positions[index] = data
        # print("CONTROLLER (" + str(index) + ") RECEIVED: " + str(data))

        self.sync_integer -= 1
        if self.sync_integer == 0:
            self.generatePositions()
            self.sync_integer = self.n_robots + 1

    def storeRawBallPosition(self, data):
        self.raw_ball_position = data
        # print("CONTROLLER (ball) RECEIVED: " + str(data))

        self.sync_integer -= 1
        if self.sync_integer == 0:
            self.generatePositions()
            self.sync_integer = self.n_robots + 1


if __name__ == "__main__":
    try:
        roscomm = RosComm("vsss_inf", robot_index_start=4)
    except rospy.ROSInterruptException:
        pass