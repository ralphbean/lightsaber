#!/usr/bin/bash

# STOMP
#ssh -t -p 330 -l rbean -L 61619:amq-fab-01-stg.mw.lab.eng.brq.redhat.com:61619 ovpn-phx2.redhat.com

# AMQP
#ssh -t -p 330 -l rbean -L 61618:amq-fab-01-stg.mw.lab.eng.brq.redhat.com:61618 ovpn-phx2.redhat.com

# Web UI
ssh -t -p 330 -l rbean -L 8181:amq-fab-01-stg.mw.lab.eng.brq.redhat.com:8181 ovpn-phx2.redhat.com
