## Four Bar Tests

A ROS2 package for testing out a 4 bar linkage.

![Alt text](./images/4Bar-Top.png "Four Bar Linkage CAD")

![Alt text](./images/Leg-Assembly.png "Qronk_leg in RVIZ")

## Dependencies

Please install [urdf_launch](https://github.com/ros/urdf_launch) in the same workspace as four_bar_tests.

## Usage

Run ```ros2 launch four_bar_tests display.launch.py model:=urdf/$$MODEL$$.urdf```

If the model is in XACRO format remember to run ``` xacro model.xacro > model.urdf```  

## Fusion Export Tips
Export Fusion models to URDF using the [fusion2urdf](https://github.com/16cra40/fusion2urdf) tool.
### Before Export
* Make sure base_link is specified
* Make sure base_link is ungrounded
* Make sure all components are unlinked

### After Export
* One link duplicates so remove by trial and error
* Rename the package in the exported XACRO to match the package


## TODO
* ~~Convert LEG_ASSEMBLY1 to Mimic joints~~
* ~~Rotate LEG_ASSEMBLY1 to be flat~~
* ~~Convert from XACRO to URDF on launch~~
* ~~Independent launch from urdf_launch~~
* Merge with main QRONK github
* Import into Gazebo
* Test on ROS2 Jazzy
* Modify the python script - package name