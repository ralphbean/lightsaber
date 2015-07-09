#!/bin/bash -x

# build the blog
pushd ~/devel/threebean-blog
git pull origin master
source ~/.virtualenvs/threebean-blog/bin/activate
blogofile build
rm -rf ~/scratch/threebean.org/blog
cp -rf _site/ ~/scratch/threebean.org/blog
deactivate
source ~/.virtualenvs/awscli/bin/activate
aws s3 sync ~/scratch/threebean.org s3://threebean.org
popd
