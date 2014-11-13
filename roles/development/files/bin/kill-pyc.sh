#!/bin/bash

find . -name "*.egg*" -exec rm -r {} \;
find . -name "__pycache__" -exec rm -r {} \;
find . -name "*.pyc" -exec rm {} \;
