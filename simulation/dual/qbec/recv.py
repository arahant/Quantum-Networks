import sys
import time
from cqc.pythonLib import CQCConnection

#
def qbec(qbit1,qbit2,qbit3):
    qbit1.cnot(qbit2)
    result1 = qbit2.measure()
    if result1 == 1:
        qbit1.cnot(qbit3)
        result2 = qbit3.measure()
        if result2 == 1:
            qbit1.X()
            return qbit1.measure()
        else:
            return qbit1.measure()
    else:
        return qbit1.measure()

#
def recv_qubit(node,sender,it,err):
    # extract the key
    qbit1 = node.recvQubit()
    key = None
    if err==0:
        key = qbit1.measure()
    elif err==1:
        qbit2 = node.recvQubit()
        qbit3 = node.recvQubit()
        key = qbec(qbit1,qbit2,qbit3)
    # print("{}:{} Received {}".format(node.name,it,key))
    print("{},{},{},{},{},{}".format(it,sender,node.name,key,err,time.time()))

#
def start():
    sender = "Node{}".format(sys.argv[1])
    recv = "Node{}".format(sys.argv[2])
    it = sys.argv[3]
    err = int(sys.argv[4])
    with CQCConnection(recv) as node:
        recv_qubit(node,sender,it,err)

#
start()
