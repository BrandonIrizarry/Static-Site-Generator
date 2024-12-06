#!/usr/bin/env bash

export PYTHONPATH="./src"
default_nickname="index"
public_dir="$HOME"/boot_dev/Static_Site_Generator/public
static_dir="$HOME"/boot_dev/Static_Site_Generator/static
tmpfile=/tmp/body.html
template="$HOME"/boot_dev/Static_Site_Generator/template.html
dest_file="$HOME"/boot_dev/Static_Site_Generator/public/index.html


# Copy static assets to public directory.
#
# This will create the public directory if it's missing, so that
# utilities from here onward can assume its existence.
python3 "$HOME"/boot_dev/Static_Site_Generator/src/create_or_copy.py "$static_dir" "$public_dir"


python3 "$HOME"/boot_dev/Static_Site_Generator/src/main.py "$default_nickname" "$tmpfile"


python3 "$HOME"/boot_dev/Static_Site_Generator/src/copy_html_to_template.py "$template" "$tmpfile" "$dest_file"

cd public && python3 -m http.server 8888
