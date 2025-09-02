cmake_minimum_required(VERSION 3.10.2)
project(ranger_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY meshes urdf launch rviz DESTINATION share/${PROJECT_NAME})

ament_package()
