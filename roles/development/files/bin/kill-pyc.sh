#!/bin/bash
find . -name "*.py[co]" -delete -or -name "__pycache__" -delete -or -name "*.egg*" -delete
