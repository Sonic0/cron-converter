#!/usr/bin/env bash

TEST_URL="https://test.pypi.org/legacy/"

pip3 install -r requirements/release.txt

[ -d "dist" ] && rm -r dist && echo -e '\e[38;5;219m./dist dir deleted\e[0m'
python3 setup.py sdist bdist_wheel
[[ "$1" = "--local" ]] && echo -e '\e[38;5;219mtar.gz created in ./dist, install it locally via pip\e[0m' && exit 0

if twine check dist/*; then
  if [ "$1" = "--test" ] ; then
    twine upload --repository-url ${TEST_URL} dist/*
  else
    twine upload dist/*
  fi
fi

