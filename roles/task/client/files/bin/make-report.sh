#!/bin/bash

today=$(date +%Y-%m-%d)
/usr/local/bin/timesheet.sh | ~/.virtualenvs/ansi2html/bin/ansi2html --linkify > /tmp/timesheet.html
cp /tmp/timesheet.html ~/scratch/threebean.org/timesheets/$today.html
cp /tmp/timesheet.html ~/scratch/threebean.org/timesheets/latest.html
rm /tmp/timesheet.html

/usr/local/bin/timesheet.sh proj:bodhi | ~/.virtualenvs/ansi2html/bin/ansi2html --linkify > /tmp/timesheet.html
cp /tmp/timesheet.html ~/scratch/threebean.org/timesheets/bodhi/$today.html
cp /tmp/timesheet.html ~/scratch/threebean.org/timesheets/bodhi/latest.html
rm /tmp/timesheet.html

source ~/.virtualenvs/awscli/bin/activate
aws s3 sync ~/scratch/threebean.org s3://threebean.org

echo "http://threebean.org/timesheets/$today.html"
echo "http://threebean.org/timesheets/bodhi/$today.html"
