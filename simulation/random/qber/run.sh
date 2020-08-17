#!/bin/sh

if [ $1 -gt 20 ]
then
    echo "Maximum allowed qubits: 20"
else
    python3 alicetest.py $1 &
    python3 bobtest.py $1 &
fi
