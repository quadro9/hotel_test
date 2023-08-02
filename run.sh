#!/bin/bash

sudo apt update
sudo apt install -y python3-pip python3-venv cmake
python3 -m pip install -U pip

if [ ! -d ".venv" ] ; then
    python3 -m venv .venv
fi

source .venv/bin/activate
python3 -m pip install pytest

mkdir -p build
cd build
cmake ..
cmake --build .

cd ..

export COMMAND_RUN="./build/bin/hotel"

python3 -m pytest --verbose --junitxml=tests/hotel_tests.xml tests/
