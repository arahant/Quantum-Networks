import sys
import time
from random import randint
from cqc.pythonLib import qubit
from cqc.pythonLib import CQCConnection

STEP_SEND_EPR = "s1"
STEP_SEND_QBT = "s2"
STEP_RECV_EPR = "s3"
STEP_RECV_QBT = "s4"

#
def process_request(node,wait,send,id2):
    # Generate random
    b0 = randint(0,1)
    b1 = randint(0,1)

    # 1. Receiving an EPR qubit or creating a new qubit
    q = None
    if wait==1:
        epr = node.recvEPR()
        id = epr._remote_entNode
        print("{},{},{},{},{},{}".format(node.name,id,STEP_RECV_EPR,time.time(),0,0))
        q = node.recvQubit()
        ts = time.time()
        q.cnot(epr)
        q.H()
        b0 = q.measure()
        b1 = epr.measure()
        print("{},{},{},{},{},{}".format(node.name,id,STEP_RECV_QBT,ts,b0,b1))

    # 2. Teleporting and Entanglement swapping
    recv = None
    epr = None
    if send==1 and id2 is not None:
        recv = "Node{}".format(id2)
        epr = node.createEPR(recv)
        print("{},{},{},{},{},{}".format(node.name,recv,STEP_SEND_EPR,time.time(),0,0))

        if b1==1:
            epr.X()
        if b0==1:
            epr.Z()
        node.sendQubit(epr,recv)
        print("{},{},{},{},{},{}".format(node.name,recv,STEP_SEND_QBT,time.time(),b0,b1))

#
def start():
    wait = int(sys.argv[1])
    send = int(sys.argv[2])
    id = "Node{}".format(sys.argv[3])
    with CQCConnection(id) as node:
        if send==1:
            process_request(node,wait,send,sys.argv[4])
        else:
            process_request(node,wait,send,None)

#
start()
