#!/usr/bin/env bash
#================================================================
# DESCRIPTION
# This script builds the Python library and uploads the package either to testPyPi or PyPi, depending on the first argument provided.
# The argument can be '--local' for local testing, '--test' for uploading to testPyPi, or left empty for uploading to PyPi.
#================================================================

print_msg() {
  local GRE='\e[1;32m'
  local NC='\e[0m'
  echo -e "${GRE}$1${NC}"
  return 0
}

pip3 install -r requirements/release.txt

[ -d "dist" ] && rm -r dist && print_msg './dist dir deleted'
python3 -m build
[[ "$1" = "--local" ]] && print_msg 'tar.gz created in ./dist, install it locally via pip' && exit 0

if twine check dist/*; then
  if [ "$1" = "--test" ] ; then
    twine upload --repository testpypi dist/*
    print_msg "Use this command for local testing:
      python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps cron-converter"
  else
    twine upload dist/*
  fi
fi

