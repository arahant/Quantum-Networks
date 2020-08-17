import sys
import time
from random import randint
from cqc.pythonLib import qubit
from cqc.pythonLib import CQCMix
from cqc.pythonLib import CQCConnection
from cqc.pythonLib import CQCMixConnection

##################################################
# Quantum coin toss
def quantum_coin_toss(node):
    q = qubit(node)
    q.H()
    coin = q.measure()
    return coin

##################################################
# Decryption message
def decrypt_enc(msg,key):
    return (msg + key) % 2

##################################################
# Decryption message
# def qbec(qb,node):

##################################################
# Achieving QKD through CHSH protocol
def qkd_chsh(voter):
    q = voter.recvQubit()
    msg = voter.recvClassical()
    # msg = decrypt_msg(msg,key)
    data = list(msg)
    bg = data[0]
    # base = quantum_coin_toss(voter)
    bv = randint(0,1)
    # print(bg,bv)
    if bg==bv:
        q.H()
        key = q.measure()
        return key
    else:
        q.release()
        return None

##################################################
# Achieving QKD through Correlated Randomness - EPR
def qkd_epr(voter):
    q = voter.recvEPR()
    key = q.measure()
    return key

##################################################
# Achieving QKD through True randomness
def qkd_rand(voter):
    # extract the key
    q = voter.recvQubit()
    k = q.measure()
    return k

##################################################
# Achieving QKD through True randomness
def qkd_rand_qber(voter,sender):
    # with CQCMixConnection(sender) as voter:
    # extract the key
    qbit1 = voter.recvQubit()
    qbit2 = voter.recvQubit()
    qbit3 = voter.recvQubit()
    qbit1.cnot(qbit2)
    result1 = qbit2.measure()
    if result1 == 1:
        qbit1.cnot(qbit3)
        result2 = qbit3.measure()
        if result2 == 1:
            qbit1.X()
            k = qbit1.measure()
            return k
        else:
            return qbit1.measure()
    else:
        return qbit1.measure()

##################################################
def start():
    sender = "Node{}".format(sys.argv[1])
    recv = "Node{}".format(sys.argv[2])
    app_id = "{}{}".format(sys.argv[2],sys.argv[1])
    with CQCConnection(sender) as voter:
        ## key = qkd_chsh(voter)
        # key = qkd_epr(voter)
        # key = qkd_rand(voter)
        key = qkd_rand_qber(voter,sender)
        print("{},{}".format(app_id,key))

#
start()
