#!/bin/sh

tmp_vote="tmp_vote.csv"
met_vote="metrics_vote.csv"
met_vote_data="metrics_vote_data.csv"
met_vote_all="metrics_vote_all.csv"
MSG_NO_TMP="No temporary vote data available"

if [ -f $tmp_vote ]
then
    python3 metrics_vote_rearrange.py $tmp_vote >> $met_vote
    python3 metrics_vote.py $met_vote > $met_vote_data
    paste -d "," $met_vote $met_vote_data > $met_vote_all
    rm $tmp_vote
else
    echo $MSG_NO_TMP
fi
