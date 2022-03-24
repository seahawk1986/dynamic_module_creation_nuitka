#!/usr/bin/bash

[ -f example.bin ] || ./build.sh

# add the bin directory to the PATH, so external_command.py can be found
PATH="$PATH:$(pwd)/bin"
# run the example
./example.bin
