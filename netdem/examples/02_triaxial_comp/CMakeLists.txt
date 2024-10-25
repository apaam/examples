cmake_minimum_required(VERSION 3.13)
project(${PROJECT_EXAMPLE_BASE_NAME}_triaxial_comp)

file(GLOB SRC_FILES "*.cpp" "*.hpp")
add_executable(${PROJECT_NAME} ${SRC_FILES})
target_include_directories(${PROJECT_NAME} PRIVATE ${NETDEM_SOURCE_DIRS}
                                                   ${DEPENDENCIES_INCLUDE_DIRS})
target_link_directories(${PROJECT_NAME} PRIVATE ${DEPENDENCIES_LIBRARY_DIRS})
target_link_libraries(${PROJECT_NAME} ${NETDEM_LIBRARY}
                      ${DEPENDENCIES_LIBRARIES})
install(
  TARGETS ${PROJECT_NAME}
  DESTINATION bin
  COMPONENT examples)
