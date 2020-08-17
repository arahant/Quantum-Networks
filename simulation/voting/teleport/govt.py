import sys
from cqc.pythonLib import CQCConnection

#
def teleport_recv():
    recv = "Node{}".format(sys.argv[1])
    # print(recv)
    with CQCConnection(recv) as govt:
        epr=govt.recvEPR()
        print("EPR received at {}".format(recv))

        data = govt.recvClassical()
        if data[0]==1:
            epr.Z()
        if data[1]==1:
            epr.X()
        print("Classical data received at {}".format(recv))

#
teleport_recv()
