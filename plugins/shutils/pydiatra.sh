#!/bin/bash



# Runs py3diatra on all python files (prerequisite: pip install pydiatra)
find . -wholename "./thirdparty" -prune -o -type f -iname "*.py" -exec py3diatra '{}' \; | grep -v bare-except
