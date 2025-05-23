#!/bin/bash



# Runs pycodestyle on all python files (prerequisite: pip install pycodestyle)
find . -wholename "./thirdparty" -prune -o -type f -iname "*.py" -exec pycodestyle --ignore=E501,E302,E305,E722,E402 '{}' \;
