#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install libpq-dev -y
CFLAGS="-Wno-narrowing" pip3 install cld2-cffi
pip install -e .