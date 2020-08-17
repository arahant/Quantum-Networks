#!/bin/sh

met_file="metrics_time.csv"
met_file_err="metrics_time_err.csv"
data_file="metrics_time_data.csv"
data_file_err="metrics_time_data_err.csv"

if [ -f $met_file ]
then
    python3 metrics.py $met_file > $data_file
fi

if [ -f $met_file_err ]
then
    python3 metrics.py $met_file_err > $data_file_err
fi
