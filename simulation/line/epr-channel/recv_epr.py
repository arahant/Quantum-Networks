import time
import cqc.pythonLib as cqc

node = "Node"

#
def recv_epr(node, id):
    # Initialize the connection
    receiver = node+id
    with cqc.CQCConnection(receiver) as Bob:
        # Receive qubit
        q=Bob.recvEPR()

        # Measure qubit
        m = q.measure()

        # Measure timestamp
        ts = time.time()

        return (receiver,m,ts)
