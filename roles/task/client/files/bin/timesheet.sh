#!/bin/bash

source /home/threebean/.bashrc

phrase="1-weeks-ago"
fmt="%Y-%m-%d"
start=$(date +$fmt -d $phrase)
end=$(date +$fmt)
filter="project.isnt:apply project.isnt:family project.isnt:xmas project.isnt:cersc project.isnt:iso project.isnt:monroe project.isnt:house project.isnt:misc project.isnt:rit project.isnt:tos-rit-projects-seminar project.isnt:music project.isnt:hfoss project.isnt:wrns"
config="rc.defaultwidth=190 rc.defaultheight=75 rc._forcecolor=yes"

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
/usr/bin/task $config $filter history
/usr/bin/task $config $filter ghistory
/usr/bin/task $config burndown
/usr/bin/task $config burndown.daily
