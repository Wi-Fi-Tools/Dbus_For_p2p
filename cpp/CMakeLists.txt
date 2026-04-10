cmake_minimum_required(VERSION 3.16)
project(NetworkManager_P2P LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Find required packages
find_package(PkgConfig REQUIRED)

# sdbus-c++ - Modern C++ D-Bus library
pkg_check_modules(SDBUS REQUIRED IMPORTED_TARGET sdbus-c++>=1.0)

# GLib for main loop
pkg_check_modules(GLIB REQUIRED IMPORTED_TARGET glib-2.0)

add_executable(nm_p2p
    src/main.cpp
    src/dbus_helpers.cpp
    src/p2p_discovery.cpp
    src/p2p_connection.cpp
)

target_include_directories(nm_p2p PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

target_link_libraries(nm_p2p PRIVATE
    PkgConfig::SDBUS
    PkgConfig::GLIB
)
