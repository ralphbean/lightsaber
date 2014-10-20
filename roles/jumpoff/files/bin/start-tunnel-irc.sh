#!/usr/bin/bash

ssh -t -p 330 -l rbean -L 6667:irc.bos.redhat.com:6667 ovpn-phx2.redhat.com
