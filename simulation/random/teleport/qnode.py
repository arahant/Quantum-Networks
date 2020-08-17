import sys
import time
from random import randint
from cqc.pythonLib import qubit
from cqc.pythonLib import CQCConnection

STEP_SEND_EPR = 1
STEP_SEND_QBT = 2
STEP_RECV_EPR = 3
STEP_RECV_QBT = 4

#
def process_request(node,wait,send,id2):
    # 1. Receiving an EPR qubit or creating a new qubit
    q = None
    if wait==1:
        q = node.recvEPR()
        id = q._remote_entNode
        # print("{}: Received an EPR from {} at {}".format(node.name,id,time.time()))
        print("{},{},{},{}".format(node.name,id,STEP_RECV_EPR,time.time()))
        data = node.recvClassical()
        # print("{}: Received classical data from {} at {}".format(node.name,id,time.time()))
        print("{},{},{},{}".format(node.name,id,STEP_RECV_QBT,time.time()))
        if data[0]==1:
            q.Z()
        if data[1]==1:
            q.X()
    else:
        q = qubit(node)

    # 2. Teleporting and Entanglement swapping
    recv = None
    epr = None
    if send==1 and id2 is not None:
        recv = "Node{}".format(id2)
        epr = node.createEPR(recv)
        # print("{}: EPR channel established with {} at {}".format(node.name,recv,time.time()))
        print("{},{},{},{}".format(node.name,recv,STEP_SEND_EPR,time.time()))

        q.cnot(epr)
        q.H()
        b1 = q.measure()
        b2 = epr.measure()

        data = [b1,b2]
        node.sendClassical(recv,data)
        # print("{}: Measured bits sent to {} at {}".format(node.name,recv,time.time()))
        print("{},{},{},{}".format(node.name,recv,STEP_SEND_QBT,time.time()))

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
