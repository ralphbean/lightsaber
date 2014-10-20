#!/bin/bash

source /home/threebean/.bashrc

phrase="1-weeks-ago"
fmt="%Y-%m-%d"
start=$(date +$fmt -d $phrase)
end=$(date +$fmt)
filter="project.isnt:apply project.isnt:family project.isnt:xmas project.isnt:cersc project.isnt:iso project.isnt:monroe project.isnt:house project.isnt:misc project.isnt:rit project.isnt:tos-rit-projects-seminar project.isnt:music project.isnt:hfoss project.isnt:wrns"

echo "    (generated at $(date))"
echo
echo " -- Tasks completed from $start to $end (back $phrase) -- "
/usr/bin/task $filter end.after:$start work_report

echo
echo 
echo " -- Upcoming tasks -- "
/usr/bin/task $filter next

echo
echo
echo " -- Summary -- "
/usr/bin/task $filter summary

echo
echo
echo " -- History -- "
/usr/bin/task $filter history
/usr/bin/task $filter ghistory
/usr/bin/task burndown.daily
/usr/bin/task burndown
