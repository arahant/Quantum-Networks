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

# Qubit Err Resilience
def qbed(q1,q2,q3):
    # 2 ancillas
    # q1 CNOT q2, q3
    q1.cnot(q2)
    q1.cnot(q3)
    return (q2,q3)

# 2(b). Receiving the EPR channel (qubit)
def retrieve_epr(voter,recv,err,file):
    epr = voter.recvEPR()
    if err==1:
        q2 = voter.recvQubit()
        q3 = voter.recvQubit()
        epr = qbec(epr,q2,q3)
    ts = time.time()
    # print("{}: Entanglement received from {} at {}".format(voter.name,recv,ts))
    output = "2b ({}),".format(ts)
    save_data(output,file)
    return epr

# 3. Casting votes
def cast_vote(voter,epr,recv,key,v0,v1,file):
    # 3. Casting votes in classical bits
    v0 = int(v0)
    v1 = int(v1)
    # print("{}: Casting votes {},{}".format(voter.name,v0,v1))
    output = "3 ({}.{}),".format(v0,v1)
    save_data(output,file)
    return v0,v1

# 4. Encoding votes into the EPR
def encode_votes(v0,v1,epr):
    if v1==1:
        epr.X()
    if v0==1:
        epr.Z()
    return epr

# 4. Superdense voting: sending encoded votes to Govt. server
def send_votes(voter,epr,recv,key,err,file):
    if err==1:
        q2 = qubit(voter)
        q3 = qubit(voter)
        (q2,q3) = qbed(epr,q2,q3)
        voter.sendQubit(epr,recv,remote_appID=key)
        voter.sendQubit(q2,recv,remote_appID=key)
        voter.sendQubit(q3,recv,remote_appID=key)
    else:
        voter.sendQubit(epr,recv,remote_appID=key)
    # print("{}: Encoded votes sent to {}".format(voter.name,recv))
    ts = time.time()
    output = "4 ({}),".format(ts)
    save_data(output,file)

# Receiving EPR (2b); Casting (3), Encoding (4) and Sending (5a) votes
def start():
    sender = "Node{}".format(sys.argv[1])
    recv = "Node{}".format(sys.argv[2])
    qkd = sys.argv[3]
    key_snd = key_recv = qkd
    v0 = sys.argv[4]
    v1 = sys.argv[5]
    err = int(sys.argv[6])
    file = sys.argv[7]

    with CQCConnection(sender,appID=int(key_snd,2)) as voter:
        # 2(b). Receiving the EPR channel (qubit)
        epr = retrieve_epr(voter,recv,err,file)
        # 3. Casting votes
        v0,v1 = cast_vote(voter,epr,recv,int(key_recv,2),v0,v1,file)
        # 4. Encoding votes into the EPR
        qb = encode_votes(v0,v1,epr)
        # 5(a). Superdense voting:
        send_votes(voter,qb,recv,int(key_recv,2),err,file)
        voter.close()

#
start()
