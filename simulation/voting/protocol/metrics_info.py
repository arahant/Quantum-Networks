import sys
import math
import numpy as np
import collections

#
def read_metrics(file):
    data = []
    try:
        with open(file,'r') as fr:
            line = fr.readline()
            while line:
                line = line = fr.readline()
                line = line.strip()
                if not line:
                    continue
                row = line.split(',')
                if len(row)==0:
                    continue
                data.append(row)
            fr.close()
            return data
    except IOError as err:
        print(err)

#
def calculate_count(data):
    cast_votes = data[2]
    recorded_votes = data[5]
    N = len(cast_votes)
    c1 = collections.Counter(cast_votes)
    c2 = collections.Counter(recorded_votes)
    return c1,c2,N

#
def calculate_entropy(c1,c2,N):
    ent1 = ent2 = 0.0
    for c in c1:
        pr = float(c1[c])/N
        lg = math.log(pr,2)
        val = pr*lg
        ent1 += val
    for c in c2:
        pr = float(c2[c])/N
        lg = math.log(pr,2)
        val = pr*lg
        ent2 += val
    ent = -ent1+ent2
    return ent

#
def calculate_info_loss(data,N):
    cast_votes = data[2]
    recorded_votes = data[5]
    diff1 = diff2 = 0
    for i in range(N):
        c1 = cast_votes[i]
        c2 = recorded_votes[i]
        if c1[0]!=c2[0] and c1[2]!=c2[2]:
            diff2+=1
        if c1[0]!=c2[0] or c1[2]!=c2[2]:
            diff1+=1
    return diff1,diff2

#
def calculate_threat_rate(qkd):
    # err_bits = [float(x) for x in qkd[2]]
    err_percent = [float(x) for x in qkd[3]]
    key_miss_p = sum(err_percent) / len(err_percent)
    return key_miss_p

#
def start():
    # information metrics
    vote_data = read_metrics(sys.argv[2])
    vote_data = np.array(vote_data)
    vote_data = vote_data.transpose()
    c1,c2,N = calculate_count(vote_data)
    ent = calculate_entropy(c1,c2,N)
    b1,b2 = calculate_info_loss(vote_data,N)
    print("Entropy diff: {}".format(ent))
    print("{} 1 qubit flips".format(b1))
    print("{} 2 qubit flips".format(b2))

    # key loss rate
    qkd_data = read_metrics(sys.argv[1])
    qkd_data = np.array(qkd_data)
    qkd_data = qkd_data.transpose()
    loss = calculate_threat_rate(qkd_data)
    print("% loss of key is {}".format(loss))

    t1 = float(b1)*loss/N
    t2 = float(b2)*loss/N
    print("Threat from loss key and 1 qubit flips: {}".format(t1*100))
    print("Threat from loss key and 2 qubit flips: {}".format(t2*100))

#
start()
