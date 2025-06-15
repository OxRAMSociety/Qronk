# Copyright 2022 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node

import xacro

def generate_launch_description():
    # Configure ROS nodes for launch

    # Setup project paths
    description_package = get_package_share_directory('qronk_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Load the URDF file from "description" package
    urdf_file  =  os.path.join(description_package, 'urdf', 'qronk.urdf.xacro')
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()
    robot_desc = xacro.process_file(urdf_file).toprettyxml(indent='  ')

    sdf_file  =  os.path.join(description_package, 'urdf', 'qronk.gazebo.xacro')
    with open(sdf_file, 'r') as infp:
        gazebo_desc = infp.read()
    gazebo_desc = xacro.process_file(sdf_file).toprettyxml(indent='  ')

    # Setup to launch the simulator and Gazebo world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': PathJoinSubstitution([
            description_package,
            'gazebo',
            'empty.sdf'
        ])}.items(),
    )

    # Takes the description and joint angles as inputs and publishes the 3D poses of the robot links
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_desc},
        ]
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )

    # Visualize in RViz
    rviz = Node(
       package='rviz2',
       executable='rviz2',
       arguments=['-d', os.path.join(description_package, 'rviz', 'urdf.rviz')],
       condition=IfCondition(LaunchConfiguration('rviz'))
    )

    # Bridge ROS topics and Gazebo messages for establishing communication
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(description_package, 'gazebo', 'sample.yaml'),
            'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output='screen'
    )

    gz_spawner = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name", "qronk",
            "-string", gazebo_desc,
        ],
        output="screen",
    )

    return LaunchDescription([
        gz_sim,
        DeclareLaunchArgument('rviz', default_value='true',
                              description='Open RViz.'),
        bridge,
        robot_state_publisher,
        joint_state_publisher_node,
        rviz,
        gz_spawner
    ])