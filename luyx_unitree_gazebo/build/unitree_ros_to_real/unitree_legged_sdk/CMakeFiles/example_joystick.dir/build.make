# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/jiaojunpeng/luyx_unitree_gazebo/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/jiaojunpeng/luyx_unitree_gazebo/build

# Include any dependencies generated for this target.
include unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/depend.make

# Include the progress variables for this target.
include unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/progress.make

# Include the compile flags for this target's objects.
include unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/flags.make

unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/example/example_joystick.cpp.o: unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/flags.make
unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/example/example_joystick.cpp.o: /home/jiaojunpeng/luyx_unitree_gazebo/src/unitree_ros_to_real/unitree_legged_sdk/example/example_joystick.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/jiaojunpeng/luyx_unitree_gazebo/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/example/example_joystick.cpp.o"
	cd /home/jiaojunpeng/luyx_unitree_gazebo/build/unitree_ros_to_real/unitree_legged_sdk && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/example_joystick.dir/example/example_joystick.cpp.o -c /home/jiaojunpeng/luyx_unitree_gazebo/src/unitree_ros_to_real/unitree_legged_sdk/example/example_joystick.cpp

unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/example/example_joystick.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/example_joystick.dir/example/example_joystick.cpp.i"
	cd /home/jiaojunpeng/luyx_unitree_gazebo/build/unitree_ros_to_real/unitree_legged_sdk && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/jiaojunpeng/luyx_unitree_gazebo/src/unitree_ros_to_real/unitree_legged_sdk/example/example_joystick.cpp > CMakeFiles/example_joystick.dir/example/example_joystick.cpp.i

unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/example/example_joystick.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/example_joystick.dir/example/example_joystick.cpp.s"
	cd /home/jiaojunpeng/luyx_unitree_gazebo/build/unitree_ros_to_real/unitree_legged_sdk && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/jiaojunpeng/luyx_unitree_gazebo/src/unitree_ros_to_real/unitree_legged_sdk/example/example_joystick.cpp -o CMakeFiles/example_joystick.dir/example/example_joystick.cpp.s

# Object files for target example_joystick
example_joystick_OBJECTS = \
"CMakeFiles/example_joystick.dir/example/example_joystick.cpp.o"

# External object files for target example_joystick
example_joystick_EXTERNAL_OBJECTS =

example_joystick: unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/example/example_joystick.cpp.o
example_joystick: unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/build.make
example_joystick: unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/jiaojunpeng/luyx_unitree_gazebo/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../example_joystick"
	cd /home/jiaojunpeng/luyx_unitree_gazebo/build/unitree_ros_to_real/unitree_legged_sdk && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/example_joystick.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/build: example_joystick

.PHONY : unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/build

unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/clean:
	cd /home/jiaojunpeng/luyx_unitree_gazebo/build/unitree_ros_to_real/unitree_legged_sdk && $(CMAKE_COMMAND) -P CMakeFiles/example_joystick.dir/cmake_clean.cmake
.PHONY : unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/clean

unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/depend:
	cd /home/jiaojunpeng/luyx_unitree_gazebo/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jiaojunpeng/luyx_unitree_gazebo/src /home/jiaojunpeng/luyx_unitree_gazebo/src/unitree_ros_to_real/unitree_legged_sdk /home/jiaojunpeng/luyx_unitree_gazebo/build /home/jiaojunpeng/luyx_unitree_gazebo/build/unitree_ros_to_real/unitree_legged_sdk /home/jiaojunpeng/luyx_unitree_gazebo/build/unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : unitree_ros_to_real/unitree_legged_sdk/CMakeFiles/example_joystick.dir/depend

