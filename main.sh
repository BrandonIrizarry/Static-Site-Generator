#!/usr/bin/env bash

export PYTHONPATH="./src"
default_nickname="index"
public_dir="$HOME"/boot_dev/Static_Site_Generator/public

mkdir "$public_dir"
python3 "$HOME"/boot_dev/Static_Site_Generator/src/main.py $default_nickname "$public_dir"/index.html

# cd public && python3 -m http.server 8888
