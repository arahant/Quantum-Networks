import sys
from cqc.pythonLib import CQCConnection

node = "Node"

#
def teleport_recv():
    recv = node+str(sys.argv[1])
    # print(recv)
    with CQCConnection(recv) as bob:
        epr=bob.recvEPR()
        print("EPR received at {}".format(recv))

        data = bob.recvClassical()
        if data[0]==1:
            epr.Z()
        if data[1]==1:
            epr.X()
        print("Classical data received at {}".format(recv))

#
teleport_recv()
