#!/usr/bin/env bash
sudo apt install python3-venv
python3.6 -m venv lang_detect_api
source lang_detect_api/bin/activate
export PYTHON_PATH="/mnt/c/Users/Supun/Documents/X5GON/API/lang_detect_api/bin"
export LANGUAGE_API_URL="http://127.0.0.1:5000/language_detection"
export FASTTEXT_MODEL_DIR="/mnt/c/Users/Supun/Documents/X5GON/API/x5gon_rest/_data" # path to repo +  X5_langdetect/x5gon_rest/_data
sudo apt-get update
sudo apt-get install libpq-dev -y
CFLAGS="-Wno-narrowing" pip3 install cld2-cffi
$PYTHON_PATH/pip install -e .