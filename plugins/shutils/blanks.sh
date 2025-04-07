#!/bin/bash


# Removes trailing spaces from blank lines inside project files
find . -type f -iname '*.py' -exec sed -i 's/^[ \t]*$//' {} \;
