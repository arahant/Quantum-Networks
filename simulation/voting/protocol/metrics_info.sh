#!/bin/sh

met_qkd_all="metrics_qkd_all.csv"
met_vote_all="metrics_vote_all.csv"

python3 metrics_info.py $met_qkd_all $met_vote_all
