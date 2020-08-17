import sys
import time
from cqc.pythonLib import qubit, CQCConnection

#
def quantum_coin_toss(node):
    q = qubit(node)
    q.H()
    c = q.measure()
    return c

#
def send_qubit_qber(node,recv,it,err):
    # generate a key bit
    # key = quantum_coin_toss(node)
    key = 0
    # generate a qubit
    q1 = qubit(node)
    # encode the key into qubit
    if key==1:
        q1.X()

    if err==1:
        # 2 ancillas
        q2 = qubit(node)
        q3 = qubit(node)
        # q1 CNOT q2, q3
        q1.cnot(q2)
        q1.cnot(q3)
        # send all 3 qubits
        node.sendQubit(q1,recv)
        node.sendQubit(q2,recv)
        node.sendQubit(q3,recv)
    else:
        node.sendQubit(q1,recv)
    # print("{}:{} Sending {} to {}".format(node.name,it,key,recv))
    print("{},{},{},{},{},{}".format(it,node.name,recv,key,err,time.time()))

#
def start():
    sender = "Node{}".format(sys.argv[1])
    recv = "Node{}".format(sys.argv[2])
    it = sys.argv[3]
    err = int(sys.argv[4])
    with CQCConnection(sender) as node:
        send_qubit_qber(node,recv,it,err)

#
start()
