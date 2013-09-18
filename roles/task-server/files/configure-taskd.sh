#!/bin/bash
# Configure taskd
cd /var/tmp
cd taskd
cd demo/server
./setup
taskd config --force --data root/ client.allow '^task [2-9],^taskd,^libtaskd,^Mirakel [1-9]'
