#!/bin/bash
# Install taskd from source
cd /var/tmp
rm -rf taskd/
git clone git://tasktools.org/taskd.git
cd taskd
git checkout d02090ba433b6ba15a64672016ae0ee056ab4328
cmake .
make
make install
