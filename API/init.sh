#!/usr/bin/env bash
sudo apt install python3-venv
python3.6 -m venv lang_detect
source lang_detect/bin/activate
export REPO_PATH="/mnt/c/Users/Supun/Documents" # change this path to your repo directory
export PYTHON_PATH=$REPO_PATH"/X5_langdetect/lang_detect/bin"
export FASTTEXT_MODEL_DIR=$REPO_PATH"/X5_langdetect/x5gon_rest/_data"
export LANGUAGE_API_URL="http://127.0.0.1:5000/language_detection"
sudo apt-get update
sudo apt-get install libpq-dev -y
CFLAGS="-Wno-narrowing" pip3 install cld2-cffi
$PYTHON_PATH/pip install -e .