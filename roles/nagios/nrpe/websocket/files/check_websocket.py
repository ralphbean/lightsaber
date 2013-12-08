#!/usr/bin/env python
""" Nagios/nrpe script to check for moksha websocket activity. """

import argparse
import json
import socket
import sys

import websocket

parser = argparse.ArgumentParser()
parser.add_argument('--timeout', type=int)
parser.add_argument('--address')
parser.add_argument('--topic')
args = parser.parse_args()

for attr in ['timeout', 'address', 'topic']:
    if not getattr(args, attr, None):
        print "UNK:  --%s is required" % attr
        sys.exit(3)

timeout = args.timeout
address = args.address
topic = args.topic

client = websocket.create_connection(address)
client.settimeout(timeout)
client.send(json.dumps(dict(
    topic="__topic_subscribe__",
    body=topic,
)))

try:
    body = client.recv()
    contents = json.loads(body)
    assert 'body' in contents
    print "OK - %r websocket message received from %r" % (topic, address)
    sys.exit(0)
except socket.timeout:
    print "CRIT - no %r websocket message received from %r in %r seconds" % (
        topic, address, timeout)
    sys.exit(2)
except Exception as e:
    print "WARN - %r" % e
    sys.exit(1)
finally:
    client.close()
