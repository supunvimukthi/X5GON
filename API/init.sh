#!/usr/bin/env bash
sudo apt install python3.6-venv
pip install virtualenv
python3.6 -m virtualenv lang_detect
source lang_detect/bin/activate
export REPO_PATH="/home/supun/Documents" # change this path to your repo directory
export PYTHON_PATH=$REPO_PATH"/X5GON/API/lang_detect/bin"
export FASTTEXT_MODEL_DIR=$REPO_PATH"/X5GON/API/x5gon_rest/_data"
export LANGUAGE_API_URL="http://127.0.0.1:5000/language_detection"
sudo apt-get update
sudo apt-get install libpq-dev -y
CFLAGS="-Wno-narrowing" pip3 install cld2-cffi
$PYTHON_PATH/pip install -e .