#!/usr/bin/env python
import rospy
from std_msgs.msg import String

from strategy import Athena
from control import Zeus


class RosComm:
    def __init__(self, node_name, pub_topic, sub_topic, n_robots, field_width, field_height, default_velocity):
        """
        Subscriber thread:
        - Receive observations
        - Process observations and holds an action

        Publisher thread: 
        - Publishes held actions and waits according to rate.
        """
        self.obs = []
        self.action = []

        # VSSS controllers
        self.athena = Athena()
        self.zeus = Zeus()
        self.athena.setup(n_robots, field_width, field_height, default_velocity)
        self.zeus.setup(n_robots)

        self.pub_topic = pub_topic
        self.sub_topic = sub_topic

        rospy.init_node(node_name, anonymous=True)
        self.subscriber()
        self.publisher()

    def publisher(self):
        pub = rospy.Publisher(self.pub_topic, String, queue_size=10)
        rate = rospy.Rate(60) # 60hz
        while not rospy.is_shutdown():
            hello_str = "hello world"
            print("CONTROLLER PUBLISHED: " + str(hello_str))
            pub.publish(hello_str)
            rate.sleep()

    def subscriber(self):
        """ 
        Gets ROS messages on simulator topic and updates corresponding actions
        """
        rospy.Subscriber(self.sub_topic, String, self.generateAction)

    def generatePositions(self):
        """
        Converts simulator positions to be used by Athena.
        Args:
            obs: simulator observation
        Returns:
            List of cartesian coordinates
        """
        pass

    def generateAction(self, data):
        """
        Gets converted simulator observations and uses VSSS controllers to 
        generate and store actions.
        """
        print("CONTROLLER RECEIVED: " + str(data))


if __name__ == "__main__":
    try:
        roscomm = RosComm("vsss_inf", "vsss_act", "vsss_obs", 3, 640, 480, 0.8)
    except rospy.ROSInterruptException:
        pass