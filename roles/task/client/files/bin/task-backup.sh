#!/bin/bash

pushd ~/.task/
git commit -a -m 'Auto commit (cron)'
#git push origin master
popd

# With inthe.am
#/usr/bin/task sync
