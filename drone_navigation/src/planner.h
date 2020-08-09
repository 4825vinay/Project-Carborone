#include<ros/ros.h>
#include<trajectory_msgs/MultiDOFJointTrajectory.h>
#include<nav_msgs/Odometry.h>
#include<geometry_msgs/Transform.h>
#include<geometry_msgs/Vector3.h>
#include<vector>

class Planner{
public:
    // Constructor
    Planner(std::string odomTopic_, std::string trajTopic_);
    // Destructor
    ~Planner();
    //Vector to store points
    std::vector<geometry_msgs::Vector3> points;
    //publish trajectory
    void publishTrajectory();

private:
    ros::NodeHandle nh;
    //ROS Publishers
    ros::Publisher trajectoryPub;

    //ROS Subscribers
    ros::Subscriber odomSub;

    //Topics
    std::string odomTopic;
    std::string trajTopic;

    
    //store position and orientaion
    geometry_msgs::Point position;
    geometry_msgs::Quaternion orientation;

    void init();
    void odomcallback(const nav_msgs::OdometryConstPtr& msg);
     

    
};
