#!/bin/bash

# This will be publishing logs locally at 5672.
# That needs to be locked down with iptables so that only pencil.rc.rit.edu can
# connect.

while [ "1" -eq "1" ] ; do
    tail \
        -F /var/log/lighttpd/access.log \
        -F /var/log/lighttpd/clamav.mirrors.rit.edu.access.log \
         2>&1 | \
        /usr/bin/narcissus-zeromq-source --targets=tcp://0.0.0.0:5672
done
