import sys
import time
from cqc.pythonLib import CQCConnection

#
def teleport_recv():
    recv = "Node{}".format(sys.argv[2])
    app_id = "{}{}".format(sys.argv[1],sys.argv[2])

    with CQCConnection(recv,appID=int(app_id)) as govt:
        # receiving the EPR connection
        epr = govt.recvEPR()
        print("{}: EPR received at {}".format(app_id,recv))
        # voter = epr.entanglement_info()
        voter_id = epr._remote_entNode

        # receiving the encoded qubit from the voter
        q = govt.recvQubit()
        ts = time.time()
        print("{}: Votes received from {} at {}".format(app_id,voter_id,ts))

        # decoding the vote
        q.cnot(epr)
        q.H()
        v0 = q.measure()
        v1 = epr.measure()
        print("{}: The received vote is {}, {}".format(app_id,v0,v1))

#
teleport_recv()
