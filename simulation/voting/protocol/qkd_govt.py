import sys
import time
from random import randint
from cqc.pythonLib import qubit
from cqc.pythonLib import CQCConnection

##################################################
# Quantum coin toss
def quantum_coin_toss(node):
    q = qubit(node)
    q.H()
    coin = q.measure()
    return coin

##################################################
# Data encryption
def encrypt_msg(key,msg):
    return (key + msg) % 2

##################################################
# Achieving QKD through CHSH protocol
# Generating: N qubits
# Sending: N qubits
def qkd_chsh(govt,sender):
    key = quantum_coin_toss(govt)
    q = qubit(govt)
    if bit==1:
        q.X()
    govt.sendQubit(q,sender)
    return bit

##################################################
# Achieving QKD through Correlated Randomness - EPR
# Generating: 2N qubits
# Sending: N qubits
# Retained: N qubits
def qkd_epr(govt,sender):
    epr = govt.createEPR(sender)
    key = epr.measure()
    return key

##################################################
# Achieving QKD through True randomness w/o Error
# Generating: N qubits + N bits
# Sending: N qubits
# Retained: N bits
def qkd_rand(govt,sender):
    # generate a key bit
    key = quantum_coin_toss(govt)
    # generate a qubit
    q = qubit(govt)
    # encode the key into qubit
    if key==1:
        q.X()
    # send the qubit
    govt.sendQubit(q,sender)
    # encode message
    # msg = randint(0,1)
    # enc = encrypt_msg(key,msg)
    # send message
    # govt.sendClassical(sender,[enc])
    return key

##################################################
# Achieving QKD through True randomness w/o Error
# Generating: 3N qubits + N bits
# Sending: 3N qubits
# Retained: N bits
def qkd_rand_qber(sender,govt):
    # generate a key bit
    key = quantum_coin_toss(govt)
    # generate a qubit
    q1 = qubit(govt)
    # encode the key into qubit
    if key==1:
        q1.X()
    # 2 ancillas
    q2 = qubit(govt)
    q3 = qubit(govt)
    # q1 CNOT q2, q3
    q1.cnot(q2)
    q1.cnot(q3)
    # send all 3 qubits
    govt.sendQubit(q1,sender)
    govt.sendQubit(q2,sender)
    govt.sendQubit(q3,sender)
    return key

##################################################
def start():
    sender = "Node{}".format(sys.argv[1])
    recv = "Node{}".format(sys.argv[2])
    app_id = "{}{}".format(sys.argv[2],sys.argv[1])
    with CQCConnection(recv) as govt:
        ## key = qkd_chsh(govt,sender,recv)
        # key = qkd_epr(govt,sender)
        # key = qkd_rand(govt,sender)
        key = qkd_rand_qber(sender,govt)
        print("{},{}".format(app_id,key))

#
start()
