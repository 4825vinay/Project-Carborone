#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Point, Twist
from nav_msgs.msg import Odometry, Path
from tf.transformations import euler_from_quaternion as efq

from collections import namedtuple

Orientation = namedtuple("Orientation", ["roll", "pitch", "yaw"])

class Controller:
    def __init__(self):
        self.position = Point()
        self.orientation = Orientation(0, 0, 0)
        self.path = []
        self.velocity = Twist()

    def __odom_callback(self, msg):
        self.position = msg.pose.pose.position
        orientatioN = efq([msg.pose.pose.orientaion.x, msg.pose.pose.orientaion.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation])
        self.orientation = Orientation(orientatioN[0], orientatioN[1], orientatioN[2])

    def __path_callback(self, msg):
        self.path = [p.pose.position for p in msg.poses]
        self.new_path_recieved = True
        self.move_bot()

    def move_bot(self):
        self.new_path_recieved = not self.new_path_recieved
        x_error = 0
        x_int = 0
        ang_error = 0
        ang_int = 0
        while self.new_path_recieved == False:
            # TODO: Complete the controller
            # Has to break when a new path is planned
            # Use PID Control
