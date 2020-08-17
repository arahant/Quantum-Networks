#!/bin/sh

# VARIABLES
GOVT="1"
key_qkd="qkd_key.key"
nodes_file="nodes.csv"
met_vote="metrics_vote.csv"
tmp_vote="tmp_vote.csv"
MSG_NO_QKD="The Quantum Key has either expired or non-existent"
MSG_INVALID_ARGS="Please ensure input is of the form: ./vote.sh <voter_id> <vote0> <vote1> (./vote.sh 2 0 1)"
MSG_INVALID_VOTER_ID="Please enter a valid voter id (not 1)"
MSG_NO_VOTE="Please provide cast 2 votes as: ./vote.sh <voter_id> <vote0> <vote1> (eg: ./vote.sh 2 0 1)"
MSG_VOTE_RANGE="Please ensure the votes are {0,1}"

if [ ! -f $key_qkd ]
then
    echo $MSG_NO_QKD
elif [ -z "$1" ]
then
    echo $MSG_INVALID_ARGS
elif [ "$1" = "1" ]
then
    echo $MSG_INVALID_VOTER_ID
elif [ -z "$3" ]
then
    echo $MSG_NO_VOTE
elif [ $2 -gt 1 ]
then
    echo $MSG_VOTE_RANGE
elif [ $3 -gt 1 ]
then
    echo $MSG_VOTE_RANGE
else
    # Remote Quantum voting protocol
    # i. Starting classical servers
    echo "Starting classical servers..."
    python3 servers.py $nodes_file

    # 1. QKD: qkd.sh
    # 1a. Getting the generated keys
    declare -A qkd
    while IFS= read -r line
    do
        IFS=':'
        read -ra keys <<< "$line"
        qkd[${keys[0]}]=${keys[1]}
    done < $key_qkd

    err=0
    if [ "$err" = "1" ]
    then
        echo "-----------------------------------------------------"
        echo "With QBEC"
    fi

    VOTER=$1
    voterid="${GOVT}${VOTER}"
    key=${qkd[$voterid]}

    echo "-----------------------------------------------------"
    echo "Casting votes of ${VOTER}"
    # echo "">$tmp_vote

    # 2. Entanglement
    # 3. Vote casting
    # 4. Votes encoding
    # 5. Superdense voting
    # 6. Decoding votes
    python3 vote_record.py $VOTER $GOVT $key $err $tmp_vote &
    python3 vote_cast.py $VOTER $GOVT $key $2 $3 $err $tmp_vote

    # Removing the stored QKD keys of the voter
    rm $key_qkd
fi
