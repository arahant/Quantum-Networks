#!/bin/sh

# Variables
met_file="metrics_raw.csv"
adj_file="adjacency_matrix.csv"
route_file="route.csv"
MSG_NO_ADJ="Please provide an adjacency matrix file in CSV format"

if [ ! -f $adj_file ]
then
    echo MSG_NO_ADJ
else
    # Calculating route from Adjacency matrix
    python3 route.py $adj_file > $route_file

    # Starting SimulaQron with custom topology from Adj matrix
    python3 topology.py $adj_file
fi
