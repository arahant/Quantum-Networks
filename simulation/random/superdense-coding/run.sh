#!/bin/sh

# Variables
met_file="metrics_raw.csv"

# Extracting routes
route_file="route.csv"
line=`cat $route_file`
IFS=','
read -ra route <<< "$line"
size=${#route[@]}
SENDER=${route[0]}
RECV=${route[$size - 1]}
SEND=1

# Starting classical servers
echo "-------------------------------------------"
echo "Starting classical servers..."
python3 simulate.py $route_file &

# Starting teleportation...
echo "-------------------------------------------"
echo "Starting Superdense coding from ${SENDER}..."
echo "-------------------------------------------"
for ((i=0;i<$(( $size - 1 ));i++))
do
    WAIT=1
    if [ $i = $SENDER ]
    then
        WAIT=0
    fi
    n1=${route[$i]}
    n2=${route[$i+1]}
    echo "Transporting qubit from ${n1} to ${n2}."
    # 1. CREATE EPR
    # 2. CREATE, ENCODE (OR SWAP) AND TELEPORT BITS
    # 3. RECEIVE EPR
    # 4. RECEIVE CLASSICAL BITS
    python3 qnode.py $WAIT $SEND $n1 $n2 >> $met_file &
done
WAIT=1
SEND=0
python3 qnode.py $WAIT $SEND $RECV >> $met_file &

echo "-------------------------------------------"
echo "Completed transmission at ${RECV}..."
echo "-------------------------------------------"
