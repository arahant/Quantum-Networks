import time
from cqc.pythonLib import qubit

################################################################################
# SERVER CORE
#
def recv_epr(bob,recv):
    q = bob.recvEPR()
    ts = time.time()
    print("EPR received at {} at time {}".format(recv,ts))
    return (q,ts)

#
def get_data(q,bob,recv):
    data = bob.recvClassical()
    print("Classical data received at {}".format(recv))
    if data[0]==1:
        q.Z()
    if data[1]==1:
        q.X()
    return (data,q)
