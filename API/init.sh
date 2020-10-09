#!/usr/bin/env bash
sudo apt install python3.6-venv
pip install virtualenv==20.0.33
python3.6 -m virtualenv lang_detect
source lang_detect/bin/activate
sudo apt-get update
sudo apt-get install libpq-dev -y
CFLAGS="-Wno-narrowing" pip3 install cld2-cffi
$PYTHON_PATH/pip install -e .