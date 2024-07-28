# this file contains a list of tools that can be activated and downloaded on-demand each tool is
# enabled during configuration by passing an additional `-DUSE_<TOOL>=<VALUE>` argument to CMake

# We allow it to be used anywhere with more configurability. # only activate tools for top level
# project if(NOT PROJECT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR) message("not top level project:
# ${PROJECT_SOURCE_DIR}, cmake source dir: ${CMAKE_SOURCE_DIR}") return() endif()

include(${CMAKE_CURRENT_LIST_DIR}/CPM.cmake)

CPMAddPackage("gh:StableCoder/cmake-scripts#24.04")

if(USE_STATIC_ANALYZER)
  if("clang-tidy" IN_LIST USE_STATIC_ANALYZER)
    set(CLANG_TIDY
        ON
        CACHE INTERNAL ""
    )
  else()
    set(CLANG_TIDY
        OFF
        CACHE INTERNAL ""
    )
  endif()
  if("iwyu" IN_LIST USE_STATIC_ANALYZER)
    set(IWYU
        ON
        CACHE INTERNAL ""
    )
  else()
    set(IWYU
        OFF
        CACHE INTERNAL ""
    )
  endif()
  if("cppcheck" IN_LIST USE_STATIC_ANALYZER)
    set(CPPCHECK
        ON
        CACHE INTERNAL ""
    )
  else()
    set(CPPCHECK
        OFF
        CACHE INTERNAL ""
    )
  endif()

  include(${cmake-scripts_SOURCE_DIR}/tools.cmake)

  if(${CLANG_TIDY})
    clang_tidy(${CLANG_TIDY_ARGS})
  endif()
  if(${IWYU})
    include_what_you_use(${IWYU_ARGS})
  endif()
  if(${CPPCHECK})
    cppcheck(${CPPCHECK_ARGS})
  endif()
endif()
