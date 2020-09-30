#!/usr/bin/env bash
PYTHON_PATH="/usr/bin"
export FASTTEXT_MODEL_DIR="/mnt/c/Users/Supun/Documents/X5GON/API/x5gon_rest/_data"
CFLAGS="-Wno-narrowing" pip3 install cld2-cffi
$PYTHON_PATH/pip3 install -e .