#!/bin/sh

# Variables
met_file_raw="metrics_raw.csv"
met_file_all="metrics_all.csv"
met_file_data="metrics_data.csv"

python3 metrics_rearrange.py $met_file_raw > $met_file_all
python3 metrics.py $met_file_all > $met_file_data
