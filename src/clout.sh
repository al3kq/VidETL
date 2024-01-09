#!/bin/bash

# Directory where the files are located
DIRECTORY="../output"

# Go to the directory
cd "$DIRECTORY"

# Find and delete files that don't start with 'foo'
find . -maxdepth 1 -type f ! -name 'gif*' -exec rm {} \;
