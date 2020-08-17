#!/bin/sh

python3 config.py "./route.csv" "./nw_config.cfg"
python3 node.py "./route.csv" "./nw_config.cfg" &
