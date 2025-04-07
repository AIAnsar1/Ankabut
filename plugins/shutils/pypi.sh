#!/bin/bash

if [ ! -f ~/.pypirc ]; then
    echo "File ~/.pypirc is missing"
    exit 1
fi

declare -x SCRIPTPATH="${0}"
SETTINGS="${SCRIPTPATH%/*}/../core/settings.py"
VERSION=$(cat $SETTINGS | grep -E "^VERSION =" | cut -d '"' -f 2 | cut -d '.' -f 1-3)
TYPE=pip
TMP_DIR=/tmp/pypi
mkdir $TMP_DIR
cd $TMP_DIR




sed -i "s/^VERSION =.*/VERSION = \"$VERSION\"/g" ../core/settings.py
sed -i "s/^TYPE =.*/TYPE = \"$TYPE\"/g" ../core/settings.py
for file in $(find sqlmap -type f | grep -v -E "\.(git|yml)"); do echo include $file >> MANIFEST.in; done
python setup.py sdist bdist_wheel
twine check dist/*
twine upload --config-file=~/.pypirc dist/*
rm -rf $TMP_DIR
