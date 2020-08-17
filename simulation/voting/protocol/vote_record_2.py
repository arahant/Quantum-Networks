import sys
import time
from cqc.pythonLib import qubit
from cqc.pythonLib import CQCConnection

#
def save_data(data,file):
    try:
        with open(file,'a') as fw:
            fw.write(data)
            fw.close()
    except IOError as err:
        print(err)

# Qubit Err Resilience
def qbed(govt,q1):
    # 2 ancillas
    q2 = qubit(govt)
    q3 = qubit(govt)
    # q1 CNOT q2, q3
    q1.cnot(q2)
    q1.cnot(q3)
    return (q2,q3)

# Qubit Err Correction
def qbec(q1,q2,q3):
    q1.cnot(q2)
    result1 = q2.measure()
    if result1 == 1:
        q1.cnot(q3)
        result2 = q3.measure()
        if result2 == 1:
            q1.X()
            return q1
        else:
            return q1
    else:
        return q1

# 2(a). Creating an Entanglement channel
def entanglement(govt,sender,key,err,output_govt):
    epr = govt.createEPR(sender,remote_appID=key)
    if err==1:
        (q2,q3) = qbed(govt,epr)
        govt.sendQubit(q2,sender,remote_appID=key)
        govt.sendQubit(q3,sender,remote_appID=key)
    ts = time.time()
    print("{}: Entanglement created with {} at {}".format(govt.name,sender,ts))
    output_govt = "{},".format(ts)
    return epr, output_govt

# 5(b). Superdense voting: receiving the encoded qubit from the voter
def receive_encoded_votes(govt,epr,sender,err,output_govt):
    votes = govt.recvQubit()
    if err==1:
        q2 = govt.recvQubit()
        q3 = govt.recvQubit()
        votes = qbec(votes,q2,q3)
    ts = time.time()
    print("{}: Votes received from {} at {}".format(govt.name,sender,ts))
    output_govt += "{},".format(ts)
    return votes, output_govt

# 6. Decoding the votes
def decode_votes(votes,govt,epr,sender,output_govt):
    votes.cnot(epr)
    votes.H()
    v0 = votes.measure()
    v1 = epr.measure()
    print("{}: The received votes from {} are {}, {}".format(govt.name,sender,v0,v1))
    output_govt += "{},{}".format(v0,v1)
    return v0,v1,output_govt

# Creating EPR (2a); Receiving (5) and Decoding (6) votes
def start():
    try:
        sender = "Node{}".format(sys.argv[1])
        recv = "Node{}".format(sys.argv[2])
        qkd = sys.argv[3]
        key_snd = key_recv = qkd
        err = int(sys.argv[4])
        fil = sys.argv[5]
        output_govt = ""

        with CQCConnection(recv,appID=int(key_recv,2)) as govt:
            # 2a. Creating entanglement channel
            epr,output_govt = entanglement(govt,sender,int(key_snd,2),err,output_govt)
            # 5(b). Superdense voting: Handling received votes
            votes,output_govt = receive_encoded_votes(govt,epr,sender,err,output_govt)
            # 6. Decoding the votes
            v0,v1,output_govt = decode_votes(votes,govt,epr,sender,output_govt)
            print(output_govt,flush=True)
            save_data(data,fil)
            govt.close()
    except Exception as err:
        print(err)

#
start()
