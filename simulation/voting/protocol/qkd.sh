#!/bin/sh

# VARIABLES
N=10
N2=15
nodes_file="nodes.csv"
key_qkd="qkd_key.key"
tmp_key_gov="tmp_key.gov"
tmp_key_ctz="tmp_key.ctz"
met_qkd="metrics_qkd.csv"

# i. Starting classical servers
echo "Starting classical servers..."
python3 servers.py $nodes_file &

# Reading nodes
line=`cat $nodes_file`
IFS=','
read -ra nodes <<< "$line"
GOVT=${nodes[0]}
size=${#nodes[@]}

if [[ $1 -gt $N ]]
then
    N=$1
fi
if [[ $2 -gt $N2 ]]
then
    N2=$2
fi

echo "" > $key_qkd

for ((n_=$N;n_<$N2;n_++))
do
    for ((n=1;n<$size;n++))
    do
        VOTER=${nodes[$n]}
        echo "Performaing Quantum Key Distribution between ${GOVT} and ${VOTER}"
        echo "" > $tmp_key_gov
        echo "" > $tmp_key_ctz
        for ((i=0;i<$n_;i++))
        do
            # Regular QKD w/ Error (QBER)
            python3 qkd_govt.py $VOTER $GOVT >> $tmp_key_gov
            python3 qkd_voter.py $VOTER $GOVT >> $tmp_key_ctz
        done
        python3 qkd_key.py $tmp_key_ctz $tmp_key_gov $VOTER $GOVT >> $key_qkd

        # QKD Error metrics
        len=$( tail -n 1 $key_qkd )
        echo "Total Key size ${n_}"
        echo "Actual Key size ${len}"
        echo "${n_},${len}" >> $met_qkd
        sed -i "" -e "$ d" $key_qkd
    done
done

rm $tmp_key_ctz
rm $tmp_key_gov
