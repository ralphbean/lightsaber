#!/bin/bash

spec=$1

srpm=$(rpmbuild -bs $spec | awk ' { print $2 } ')
srpm=$(python -c "import os.path; print os.path.relpath('$srpm')")

cp $spec ~/scratch/threebean.org/rpm/SPECS/.
cp $srpm ~/scratch/threebean.org/rpm/SRPMS/.

# Buckets -> Duckets
/home/threebean/.virtualenvs/awscli/bin/aws s3 sync \
    ~/scratch/threebean.org/ s3://threebean.org

echo "Spec URL: http://threebean.org/rpm/$spec"
echo "SRPM URL: http://threebean.org/rpm/$srpm"
