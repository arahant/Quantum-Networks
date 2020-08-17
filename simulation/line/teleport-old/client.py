import time
from cqc.pythonLib import qubit

################################################################################
# CLIENT CORE
#
def create_qubit(alice):
    q = qubit(alice)
    q.H()
    q.X()
    return q

#
def create_epr(alice, sender, recv):
    ts = time.time()
    q = alice.createEPR(recv)
    print("EPR created at {} at time {}".format(sender,ts))
    return (q,ts)

#
def apply_locc(q1,qb):
    q1.cnot(qb)
    q1.H()
    b1 = q1.measure()
    b2 = qb.measure()
    return (b1,b2)

#
def send_info(alice,recv,b1,b2):
    data = [b1,b2]
    # data.append(info)
    # data.append(-1)
    # data.append(route)
    yield alice.sendClassical(recv,data)
