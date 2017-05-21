cmake_minimum_required(VERSION 2.8.3)
project(mines)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  std_msgs
  geometry_msgs
  rospy
  nav_msgs
  message_generation
)



#catkin_python_setup()


###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  ${catkin_INCLUDE_DIRS}
)


add_message_files(
	FILES
	environment.msg
	objective.msg
	subobjective.msg
	region_state.msg
	objective_state.msg
	region.msg
	task.msg
	trajectory.msg
	map_info.msg
	uuv_data.msg
	performance.msg
	beta_set.msg
	beta.msg
	claimed_objective.msg
	collective_beta.msg
	collective_interaction.msg
	interaction_list.msg
	interaction_set.msg
	collective_trajectories.msg)
                                        #PoseWithName.msg

#add_message_files( DIRECTORY msg FILES  pathData.msg )
                                        #PoseWithName.msg

generate_messages(
  DEPENDENCIES
  std_msgs
#  geometry_msgs
)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES polyhedral_terrains_demo
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib
   CATKIN_DEPENDS message_runtime
)




###########
## Build ##
###########

file(GLOB_RECURSE HEADER_FILES include/*.h)


  catkin_install_python(PROGRAMS
    src/main.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  )
  catkin_install_python(PROGRAMS
    src/agent_standard.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  )

  catkin_install_python(PROGRAMS
    src/draw.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  )








