#!/usr/bin/bash

# STOMP
#ssh -t -p 330 -l rbean \
#    -L 61617:fuse-fabric-01.app.eng.brq.redhat.com:61617 \
#    ovpn-phx2.redhat.com
ssh -t -p 330 -l rbean \
    -L 61617:fuse-fabric-01-stg.jboss.org:61617 \
    ovpn-phx2.redhat.com
#ssh -t -p 330 -l rbean \
#    -L 61617:fuse-fabric-01.app.eng.brq.redhat.com:61617 \
#    -L 61618:fuse-fabric-02.app.eng.brq.redhat.com:61617 \
#    -L 61619:fuse-fabric-03.app.eng.brq.redhat.com:61617 \
#    ovpn-phx2.redhat.com
