import rospy
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Header

def publish_transforms():
    t1 = TransformStamped()
    t1.header = Header(frame="base_link")
    t1