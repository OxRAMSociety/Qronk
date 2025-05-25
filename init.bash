# Install rosdep
apt-get install python3-rosdep

# Initialize rosdep
sudo rosdep init
rosdep update

# Install dependencies for all packages
# rosdep install --from-path ./qronk_control/ -y --ignore-src
# rosdep install --from-path ./qronk_description/ -y --ignore-src
# rosdep install --from-path ./qronk_gazebo/ -y --ignore-src
# rosdep install --from-path ./qronk_interfaces/ -y --ignore-src
# rosdep install --from-path ./qronk_motors/ -y --ignore-src
# rosdep install --from-path ./qronk_pybullet/ -y --ignore-src


