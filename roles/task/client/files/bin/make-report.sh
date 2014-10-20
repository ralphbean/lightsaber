#!/bin/bash

today=$(date +%Y-%m-%d)
/home/threebean/bin/timesheet.sh | ansi2html --linkify > /tmp/timesheet.html
scp /tmp/timesheet.html threebean.org:~/webapps/static/timesheets/$today.html
scp /tmp/timesheet.html threebean.org:~/webapps/static/timesheets/latest.html
rm /tmp/timesheet.html

echo "http://threebean.org/timesheets/$today.html"
