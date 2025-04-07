#!/bin/bash



find . -wholename "./thirdparty" -prune -o -type f -iname "*.py" -exec pylint --rcfile=./.pylintrc '{}' \;
