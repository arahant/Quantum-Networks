import sys
import time
from cqc.pythonLib import CQCConnection

#
def teleport_send():
    sender = "Node{}".format(sys.argv[1])
    recv = "Node{}".format(sys.argv[2])
    remote_app_id = "{}{}".format(sys.argv[1],sys.argv[2])

    with CQCConnection(sender) as voter:
        # Entangled state (EPR) created between voter and govt server
        epr = voter.createEPR(recv,remote_appID=int(remote_app_id))
        ts = time.time()
        print("{}: EPR created on {} at {}".format(remote_app_id,sender,ts))

        # votes in classical bits
        v0 = int(sys.argv[3])
        v1 = int(sys.argv[4])

        # voter encoding votes into the EPR
        if v1==1:
            epr.X()
        if v0==1:
            epr.Z()

        # sending encoded qubit to govt server
        voter.sendQubit(epr,recv,remote_appID=int(remote_app_id))
        print("{}: Encoded votes sent to {}".format(remote_app_id,recv))

#
teleport_send()
