cmake_minimum_required(VERSION 3.14...3.22)

project(BeanServer LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
if(CMAKE_EXPORT_COMPILE_COMMANDS)
  set(CMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES ${CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES})
endif()
# ---- Tools ----
include(../cmake/tools.sanitizers.cmake)
include(../cmake/tools.ccache.cmake)

# ---- Dependencies ----

include(../cmake/CPM.cmake)

CPMAddPackage(
  NAME cxxopts
  GITHUB_REPOSITORY jarro2783/cxxopts
  VERSION 3.0.0
  OPTIONS "CXXOPTS_BUILD_EXAMPLES NO" "CXXOPTS_BUILD_TESTS NO" "CXXOPTS_ENABLE_INSTALL YES"
)

CPMAddPackage(NAME BeanBackend SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/..)

# ---- Create standalone executable ----

file(GLOB sources CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/source/*.cpp)

# include(../cmake/tools.static-analyzers.cmake)
add_executable(${PROJECT_NAME} ${sources})
# include(../cmake/tools.static-analyzers.disable.cmake)

set_target_properties(
  ${PROJECT_NAME} PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED ON CXX_EXTENSIONS OFF
                             OUTPUT_NAME "BeanServer"
)

if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR CMAKE_CXX_COMPILER_ID MATCHES "GNU")
  target_compile_options(${PROJECT_NAME} PUBLIC -Wall -Wpedantic -Wextra -Werror -Weffc++)
  target_compile_options(BeanBackend PUBLIC -Wall -Wpedantic -Wextra -Werror -Weffc++)
elseif(MSVC)
  target_compile_options(${PROJECT_NAME} PUBLIC /W4 /WX)
  target_compile_options(BeanBackend PUBLIC /W4 /WX)
endif()
target_link_libraries(${PROJECT_NAME} PRIVATE BeanBackend cxxopts)
