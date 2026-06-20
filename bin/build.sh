#!/usr/bin/env bash
set -e
# This is a simple script to make it easier for me to develop project
# in the same structure repeatedly

CUR_DIR_FULL_PATH=$(dirname $(readlink -f "$0"))

# Colors
GREEN="\033[0;32m"
CYAN="\033[0;36m"
NO_COLOR="\033[0m"


function install {
  echo -e "${CYAN}Installing${NO_COLOR}"
  hatch run default:sync-venv
  hatch run notebook:sync-venv
  hatch run build-tools:sync-venv
}

function test {
  echo -e "${GREEN}Running test${NO_COLOR}"
  hatch run build-tools:test
}

function build_development {
  echo -e "${GREEN}Building for development${NO_COLOR}"
  hatch run notebook:start-lab
}

function build_release {
  echo -e "${GREEN}Building for release${NO_COLOR}"
  hatch build
}

function clean {
  echo -e "${GREEN}Running clean${NO_COLOR}"
  rm -rf .venv dist build
  find . \
    \( \
      -name ".*_cache" \
      -o -name ".ipynb_checkpoints" \
      -o -name ".jupyter*" \
    \) \
    -exec rm -rf {} +
}

function print_usage {
  echo -e "${CYAN}USAGE:${NO_COLOR}"
  echo
  echo -e "    bin/build.sh [install,test,dev,release,clean]"
  echo
}

case "$1" in
  "install")
    install
    ;;
  "test")
    test
    ;;
  "dev")
    build_development
    ;;
  "release")
    build_release
    ;;
  "clean")
    clean
    ;;
  *)
    print_usage
    ;;
esac
