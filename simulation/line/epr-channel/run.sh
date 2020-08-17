#!/bin/sh

# simulate
for n in {0..8}
do
    python3 sender.py $n $(( $n + 1 ))
    python3 recv.py $(( $n + 1 ))
done

# calculate metrics
python3 metrics_nw.py
