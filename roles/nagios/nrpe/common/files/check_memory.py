#!/usr/bin/env python

import argparse
import subprocess as sp
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--warning', default=60, type=int,
                    help="WARN if percent memory is used.")
parser.add_argument('-c', '--critical', default=80, type=int,
                    help="CRIT if percent memory is used.")
parser.add_argument('-s', '--swap', default=False, action='store_true',
                    help="Check swap instead of memory.")
args = parser.parse_args()

if args.warning >= args.critical:
    print "UNKNOWN: --warning must be less than --critical"
    sys.exit(3)

proc = sp.Popen(['free'], stdout=sp.PIPE, stderr=sp.PIPE)
stdout, stderr = proc.communicate()
if proc.returncode != 0:
    print "UNKOWN: 'free' return code was %r" % proc.returncode
    sys.exit(3)

headers, memory, swap = stdout.strip().split('\n')

if args.swap:
    name, target = 'swap', swap
else:
    name, target = 'memory', memory

total, used, free = map(int, target.split()[1:4])
percent = 100 * float(used) / float(total)

if percent > args.critical:
    print "CRITICAL:  %0.1f percent of %s used." % (percent, name)
    sys.exit(2)

if percent > args.warning:
    print "WARNING:  %0.1f percent of %s used." % (percent, name)
    sys.exit(1)

print "OKAY:  %0.1f percent of %s used." % (percent, name)
sys.exit(0)
