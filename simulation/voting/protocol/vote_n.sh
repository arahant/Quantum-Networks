#!/bin/bash

# VARIABLES
N=20
i=0
key_qkd="qkd_key.key"
nodes_file="nodes.csv"
votes_file="votes.csv"
met_vote="metrics_vote.csv"
tmp_vote="tmp_vote.csv"
MSG_NO_QKD="The Quantum Key has either expired or non-existent"
MSG_NO_VOTE="Please provide cast 2 votes as: ./vote.sh <vote0> <vote1> (eg: ./vote.sh 0 0)"
MSG_VOTE_RANGE="Please ensure the votes are {0,1}"

if [[ $1 -gt $N ]]
then
    N=$1
fi
echo "">$tmp_vote

if [ ! -f $key_qkd ]
then
    echo $MSG_NO_QKD
else
    line=`cat $nodes_file`
    IFS=','
    read -ra nodes <<< "$line"
    GOVT=${nodes[0]}
    size=${#nodes[@]}
    size=$(( size - 1 ))
    declare -A votes_list

    echo "-------------------------------------------------------------"
    echo "Simulating Quantum Voting for ${size} voters..."
    echo "-------------------------------------------------------------"

    # i. Starting classical servers
    echo "Starting classical servers..."
    # python3 servers.py $nodes_file

    # 1. QKD: qkd.sh
    # 1a. Getting the generated keys
    while IFS= read -r line
    do
        IFS=':'
        read -ra keys <<< "$line"
        if [ ! -z "$line" ]
        then
            # Generating random votes for every new set of QKD keys
            if [ $i = 0 ]
            then
                echo "-----------------------------------------------------"
                echo "Generating random votes..."
                python3 votes_random.py $nodes_file > $votes_file

                # Getting the votes from random votes file
                declare -A votes_list
                while IFS= read -r line
                do
                    IFS=':'
                    read -ra votes <<< "$line"
                    votes_list[${votes[0]}]=${votes[1]}
                done < $votes_file
            fi

            err=0
            if [ "$err" = "1" ]
            then
                echo "-----------------------------------------------------"
                echo "With QBEC"
            fi

            id=${keys[0]}
            key=${keys[1]}
            VOTER=${id:1:1}
            IFS=','
            read -ra votes <<< "${votes_list[$VOTER]}"
            v0=${votes[0]}
            v1=${votes[1]}
            echo "-----------------------------------------------------"
            echo "Casting votes of ${VOTER}"

            if [ -z "$v0" ]
            then
                echo $MSG_NO_VOTE
            elif [ -z "$v1" ]
            then
                echo $MSG_NO_VOTE
            elif [ $v0 -gt 1 ]
            then
                echo $MSG_VOTE_RANGE
            elif [ $v1 -gt 1 ]
            then
                echo $MSG_VOTE_RANGE
            else
                # 1. QKD: qkd.sh
                # 2. Entanglement
                # 3. Vote casting
                # 4. Votes encoding
                # 5. Superdense voting
                # 6. Decoding votes
                python3 vote_record.py $VOTER $GOVT $key $err $tmp_vote &
                python3 vote_cast.py $VOTER $GOVT $key $v0 $v1 $err $tmp_vote
            fi

            i=$(( i + 1 ))
            i=$(( i % $size ))
        fi
    done < $key_qkd
    # Removing the stored QKD keys of voters
    rm $votes_file
    rm $key_qkd
fi
