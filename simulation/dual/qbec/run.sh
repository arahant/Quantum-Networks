#!/bin/sh

N=10
n1=0
n2=1
err=0
met_file="metrics_time.csv"

if [ $1 -gt $N ]
then
    N=$1
fi

if [ $err = 1 ]
then
    echo "With QBEC"
    met_file="metrics_time_err.csv"
fi

echo "Running ${N} simulations..."
for((i=0;i<$N;i++))
do
    echo "Simulation ${i}"
    python3 sender.py $n1 $n2 $i $err >> $met_file
    python3 recv.py $n1 $n2 $i $err >> $met_file &
done
