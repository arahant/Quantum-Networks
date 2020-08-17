#!/bin/sh

met_qkd="metrics_qkd.csv"
met_qkd_err="metrics_qkd_data.csv"
met_qkd_all="metrics_qkd_all.csv"

python3 metrics_qkd.py $met_qkd > $met_qkd_err
paste -d "," $met_qkd $met_qkd_err > $met_qkd_all
