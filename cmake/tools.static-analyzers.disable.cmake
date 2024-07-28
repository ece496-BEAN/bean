include(${CMAKE_CURRENT_LIST_DIR}/CPM.cmake)
CPMAddPackage("gh:StableCoder/cmake-scripts#24.04")
include(${cmake-scripts_SOURCE_DIR}/tools.cmake)

reset_clang_tidy()
reset_include_what_you_use()
reset_cppcheck()
