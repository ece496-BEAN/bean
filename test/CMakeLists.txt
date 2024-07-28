cmake_minimum_required(VERSION 3.14...3.22)

project(BeanBackendTests LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
if(CMAKE_EXPORT_COMPILE_COMMANDS)
  set(CMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES ${CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES})
endif()

# ---- Options ----

option(ENABLE_TEST_COVERAGE "Enable test coverage" OFF)
option(TEST_INSTALLED_VERSION "Test the version found by find_package" OFF)

# ---- Tools ----
include(../cmake/tools.sanitizers.cmake)
include(../cmake/tools.ccache.cmake)
include(../cmake/tools.code-coverage.cmake)
# ---- Dependencies ----

include(../cmake/CPM.cmake)

CPMAddPackage("gh:doctest/doctest@2.4.9")
CPMAddPackage("gh:TheLartians/Format.cmake@1.7.3")

if(TEST_INSTALLED_VERSION)
  find_package(BeanBackend REQUIRED)
else()
  CPMAddPackage(NAME BeanBackend SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/..)
endif()

# ---- Create binary ----

file(GLOB sources CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/source/*.cpp)
include(../cmake/tools.static-analyzers.cmake)
add_executable(${PROJECT_NAME} ${sources})
include(../cmake/tools.static-analyzers.disable.cmake)

target_link_libraries(${PROJECT_NAME} doctest::doctest BeanBackend::BeanBackend)
set_target_properties(
  ${PROJECT_NAME} PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED ON CXX_EXTENSIONS OFF
)

# enable compiler warnings
if(NOT TEST_INSTALLED_VERSION)
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    target_compile_options(BeanBackend PUBLIC -Wall -Wpedantic -Wextra -Werror -Weffc++)
    target_compile_options(${PROJECT_NAME} PUBLIC -Wall -Wpedantic -Wextra -Werror -Weffc++)
  endif()
endif()

# ---- Add BeanBackendTests ----

enable_testing()

# Note: doctest and similar testing frameworks can automatically configure CMake tests. For other
# testing frameworks add the tests target instead: add_test(NAME ${PROJECT_NAME} COMMAND
# ${PROJECT_NAME})

include(${doctest_SOURCE_DIR}/scripts/cmake/doctest.cmake)
doctest_discover_tests(${PROJECT_NAME})

# ---- code coverage ----
target_code_coverage(BeanBackend)
target_code_coverage(${PROJECT_NAME} EXCLUDE .*_dep.* .*test/source.*)
# if(ENABLE_TEST_COVERAGE)
#   target_compile_options(BeanBackend PUBLIC -O0 -g -fprofile-arcs -ftest-coverage)
#   target_link_options(BeanBackend PUBLIC -fprofile-arcs -ftest-coverage)
# endif()
