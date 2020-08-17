#!/bin/sh

# starting classical servers
route_file="route.csv"
python3 simulate.py "0" "1" &
python3 voter.py "0" "1" &
python3 govt.py "1"
