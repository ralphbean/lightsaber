#!/bin/bash

# build the blog
ssh threebean.org "cd threebean-blog; git pull origin master; source ~/.virtualenvs/blog/bin/activate; blogofile build; echo done"
