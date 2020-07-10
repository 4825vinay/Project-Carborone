
# Project---Carborone
An Autonomous flying car with Deep learning based landing and take off abilities
(Project under progress)

# Instructions 
1. Install python-catkin-tools using
`sudo apt-install python-catkin-tools`
2. To clone the repo
    1. Make an new workspace

        ```
        mkdir carborone_ws    
        cd carborone_ws
        mkdir src
        cd src
        ```
    
    2. Clone the repository

        ```
        git clone https://github.com/4825vinay/Project-Carborone.git
        ```

    3. Go to workspace 

        ```
        cd ..
        catkin build
        ```
3. To use the robot in gazebo
    1. Go to workspace
    2. Source the workspace
    ```source devel/setup.bash```
    3. Launch the simulation
    ```roslaunch car_description sim.launch```

# Package 
At present the package contains URDF regarding the base of the bot
