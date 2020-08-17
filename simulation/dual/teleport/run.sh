#!/bin/sh

# starting classical servers
route_file="route.csv"
python3 simulate.py $route_file &
python3 sender.py "0" "1" &
python3 receiver.py "1"
