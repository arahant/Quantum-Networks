import sys
from cqc.pythonLib import CQCConnection
from cqc.pythonLib import qubit

node = "Node"

#
def get_qubit(alice):
    q = qubit(alice)
    q.H()
    q.X()
    print("Qubit created at {}".format(alice.name))
    return q

#
def teleport_send():
    sender = node+str(sys.argv[1])
    recv = node+str(sys.argv[2])

    with CQCConnection(sender) as alice:
        q = get_qubit(alice)

        epr = alice.createEPR(recv)
        print("EPR created at {}".format(sender))

        q.cnot(epr)
        q.H()
        b1 = q.measure()
        b2 = epr.measure()

        data = [b1,b2]
        alice.sendClassical(recv,data)
        print("Measured bits sent to {}".format(recv))

#
teleport_send()
