#!/bin/bash

spec=$1

srpm=$(rpmbuild -bs $spec | awk ' { print $2 } ')
srpm=$(python -c "import os.path; print os.path.relpath('$srpm')")

scp $spec threebean.org:~/webapps/static/rpm/SPECS/.
scp $srpm threebean.org:~/webapps/static/rpm/SRPMS/.

echo "Spec URL: http://threebean.org/rpm/$spec"
echo "SRPM URL: http://threebean.org/rpm/$srpm"
