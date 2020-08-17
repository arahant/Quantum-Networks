#!/bin/sh

# Variables
met_file_raw="metrics_raw.csv"
met_file_all="metrics_all.csv"
met_file_node="metrics_node.csv"
met_file_epr="metrics_epr.csv"

python3 metrics_rearrange.py $met_file_raw > $met_file_all
python3 metrics_node.py $met_file_all > $met_file_node
python3 metrics_channel.py $met_file_all > $met_file_epr