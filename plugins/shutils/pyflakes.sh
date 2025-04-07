#!/bin/bash



# Runs pyflakes on all python files (prerequisite: apt-get install pyflakes)
find . -wholename "./thirdparty" -prune -o -type f -iname "*.py" -exec pyflakes3 '{}' \; | grep -v "redefines '_'"
