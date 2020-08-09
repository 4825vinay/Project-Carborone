#include<ros/ros.h>
#include<trajectory_msgs/MultiDOFJointTrajectory.h>
#include<trajectory_msgs/MultiDOFJointTrajectoryPoint.h>
#include<geometry_msgs/Vector3.h>
#include<geometry_msgs/Transform.h>
#include<vector>
#include<iostream>
#include<cmath>

#include "planner.h"

Planner::Planner(std::string odomTopic_, std::string trajTopic_){
    odomTopic = odomTopic_;
    trajTopic = trajTopic_;

    init();
}
Planner::~Planner(){}

void Planner::init(){
    odomSub = nh.subscribe(odomTopic, 1, &Planner::odomcallback, this);
    trajectoryPub = nh.advertise<trajectory_msgs::MultiDOFJointTrajectory>(trajTopic, 1);
    ROS_INFO("Initialised pubs and subs");
}
void Planner::odomcallback(const nav_msgs::OdometryConstPtr& msg){
    position = msg->pose.pose.position;
    orientation = msg->pose.pose.orientation;
    publishTrajectory();
}
void Planner::publishTrajectory(){
    trajectory_msgs::MultiDOFJointTrajectory msg;
    trajectory_msgs::MultiDOFJointTrajectoryPoint point;
    for(int i = 0; i<points.size();i++){
        geometry_msgs::Transform transform;
        transform.translation = points[i];
        point.transforms.push_back(transform);
    }
    msg.points.push_back(point);
    trajectoryPub.publish(msg);
    ROS_INFO_ONCE("Published Message");
}

int main(int argc, char **argv){
    ros::init(argc, argv, "trajPub");
    Planner planner("/firefly/ground_truth/odometry", "/firefly/command/trajectory");
    geometry_msgs::Vector3 point;
    point.x = 2;
    point.y = 3;
    point.z = 5;
    planner.points.push_back(point);

    ros::spin();
}
