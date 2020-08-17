#!/bin/sh

# starting classical servers
route_file="route.csv"
python3 simulate.py "0" "1" "2" &
v1=1
v2=1
python3 voter.py "0" "1" $v1 $v2 &
python3 govt.py "0" "1" &
v1=1
v2=0
python3 voter.py "2" "1" $v1 $v2 &
python3 govt.py "2" "1" &
