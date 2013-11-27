#!/bin/bash
# Install taskd from source
cd /srv
rm -rf taskd/
git clone git://tasktools.org/taskd.git
cd taskd

# Just build the latest
#git checkout 1.0.0

cmake .
make
make install
