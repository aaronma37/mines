cmake_minimum_required(VERSION 2.8.3)
project(mines)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  std_msgs
  geometry_msgs
  rospy
  nav_msgs
)



#catkin_python_setup()

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES polyhedral_terrains_demo
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  ${catkin_INCLUDE_DIRS}
)




#add_message_files( DIRECTORY msg FILES  pathData.msg )
                                        #PoseWithName.msg

#generate_messages(
#  DEPENDENCIES
#  std_msgs
#  geometry_msgs
#)




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
    src/mobile_buoy_standard.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  )
  catkin_install_python(PROGRAMS
    src/draw.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  )

  catkin_install_python(PROGRAMS
    src/agent_standard_pre_trainer.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  )

  catkin_install_python(PROGRAMS
    src/main_pre_trainer.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  )










