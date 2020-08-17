#!/bin/sh

# simulate
input="./route.csv"
while IFS= read -r line
do
    nodes=$(echo "$line" | tr "," ",")
    for n in $nodes
    do
        echo $n
    done
done < "$input"
