#!/bin/bash -xe


export CC=gcc-15
export CXX=g++-15


sudo apt install gcc g++-15 curl git libssl-dev nvidia-cuda-toolkit colmap cmake ninja-build libeigen3-dev libceres-dev \
 libboost-all-dev libsqlite3-dev libcgal-dev libglew-dev libmetis-dev libfreeimage-dev

[ -d "$HOME/git" ] || mkdir $HOME/git
cd $HOME/git

git clone https://github.com/colmap/glomap.git
cd glomap
mkdir build
cd build

cmake .. -GNinja \
  -DCMAKE_CXX_IMPLICIT_LINK_DIRECTORIES="/usr/lib/x86_64-linux-gnu;/usr/lib;/lib/x86_64-linux-gnu;/lib;/usr/lib/gcc/x86_64-linux-gnu/15" \
  -DCMAKE_C_IMPLICIT_LINK_DIRECTORIES="/usr/lib/x86_64-linux-gnu;/usr/lib;/lib/x86_64-linux-gnu;/lib;/usr/lib/gcc/x86_64-linux-gnu/15" \
  -DCMAKE_INSTALL_PREFIX=$HOME/opt/glomap
# Broken build on ubuntu 25.10

sed -i 's|/usr/lib/gcc/x86_64-linux-gnu/13|/usr/lib/gcc/x86_64-linux-gnu/15|g' build.ninja

#cmake .. -GNinja \
#  -DBUILD_SHARED_LIBS=OFF \
#  -DCMAKE_FIND_LIBRARY_SUFFIXES=".a"
ninja # -v
ninja install
