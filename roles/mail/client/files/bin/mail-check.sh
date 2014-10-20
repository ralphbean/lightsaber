#!/bin/bash

# Using mbsync/isync now-a-days..
#/usr/bin/offlineimap
/usr/bin/mbsync -a

/usr/bin/notmuch new
