#!/bin/bash
# Create user
cd /srv/taskd/demo/server
wget http://mirakel.azapps.de/scripts/add_user.sh
chmod +x add_user.sh

# This takes user input..
echo "{{ username }}
{{ username }}" | ./add_user.sh

# Put the finishing touch on
IP_ADDR=$(ifconfig | grep inet | head -1 | awk ' { print $2 } ')
sed -i "s/localhost/${IP_ADDR}/g" {{ username }}.taskdconfig

# This also needs to happen, although it doesn't have anything to do with creating a user.
sed -i "s/localhost/${IP_ADDR}/g" root/config
