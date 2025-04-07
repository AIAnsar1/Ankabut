#!/bin/bash



find . -type d -name "__pycache__" -exec rm -rf {} \; &>/dev/null
find . -name "*.pyc" -exec rm -f {} \; &>/dev/null
