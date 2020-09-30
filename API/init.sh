#!/usr/bin/env bash

PYTHON_PATH="/usr/local/bin"

CFLAGS="-Wno-narrowing" pip install cld2-cffi
$PYTHON_PATH/pip install -e .