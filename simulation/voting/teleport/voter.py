import sys
from cqc.pythonLib import CQCConnection
from cqc.pythonLib import qubit

#
def get_qubit(voter):
    q = qubit(voter)
    q.H()
    q.X()
    print("Qubit created at {}".format(voter.name))
    return q

#
def teleport_send():
    sender = "Node{}".format(sys.argv[1])
    recv = "Node{}".format(sys.argv[2])

    with CQCConnection(sender) as voter:
        q = get_qubit(voter)

        epr = voter.createEPR(recv)
        print("EPR created at {}".format(sender))

        q.cnot(epr)
        q.H()
        b1 = q.measure()
        b2 = epr.measure()

        data = [b1,b2]
        voter.sendClassical(recv,data)
        print("Measured bits sent to {}".format(recv))

#
teleport_send()
