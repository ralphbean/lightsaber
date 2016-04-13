#!/bin/bash

source /home/threebean/.bashrc

phrase="1-weeks-ago"
fmt="%Y-%m-%d"
start=$(date +$fmt -d $phrase)
end=$(date +$fmt)
# when I started my new job.
epoch="2016-04-11"
filter="project.isnt:family project.isnt:xmas project.isnt:cersc project.isnt:iso project.isnt:house project.isnt:wrns $1"
config="rc.defaultwidth=180 rc.defaultheight=75 rc._forcecolor=yes"

echo "    (generated at $(date))"
echo
echo " -- Tasks completed from $start to $end (back $phrase) -- "
/usr/bin/task $config $filter end.after:$start work_report

echo
echo 
echo " -- Upcoming tasks -- "
/usr/bin/task $config $filter next

echo
echo
echo " -- Summary -- "
/usr/bin/task $config $filter summary

echo
echo
echo " -- History -- "
/usr/bin/task $config entry.after:$epoch $filter history
/usr/bin/task $config entry.after:$epoch $filter ghistory
/usr/bin/task $config entry.after:$epoch $1 burndown.monthly
/usr/bin/task $config entry.after:$epoch $1 burndown
/usr/bin/task $config entry.after:$epoch $1 burndown.daily
