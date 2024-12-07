#!/usr/bin/env bash

export PYTHONPATH="./src"
default_nickname="index"
public_dir="$HOME"/boot_dev/Static_Site_Generator/public
static_dir="$HOME"/boot_dev/Static_Site_Generator/static
content_dir="$HOME"/boot_dev/Static_Site_Generator/content

tmpfile=/tmp/body.html
template="$HOME"/boot_dev/Static_Site_Generator/template.html
dest_file="$HOME"/boot_dev/Static_Site_Generator/public/index.html


python3 "$HOME"/boot_dev/Static_Site_Generator/src/create_or_copy.py\
        "$static_dir"\
        "$public_dir"\
        --bootstrap


python3 "$HOME"/boot_dev/Static_Site_Generator/src/create_or_copy.py\
        "$content_dir"\
        "$public_dir"\
        --template "$template"


cd public && python3 -m http.server 8888
