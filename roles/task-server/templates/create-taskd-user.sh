#!/bin/bash
# Create user
cd /var/tmp/taskd/demo/server
wget http://mirakel.azapps.de/scripts/add_user.sh
chmod +x add_user.sh

# This takes user input..
echo {{ username }} | ./add_user.sh
