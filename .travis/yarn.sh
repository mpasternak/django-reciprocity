#!/bin/bash

set -o errexit

main() {
  setup_dependencies

  echo "INFO:
  Done! Finished setting up Travis-CI machine.
  "
}

# Takes care of updating any dependencies that the
# machine needs.
setup_dependencies() {
  echo "INFO:
  Setting up dependencies.
  "

  curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
  
  echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
  
  sudo apt-get update && sudo apt-get install -y yarn

  /usr/bin/yarn --version
  yarn --version
  whereis yarn
}

main
