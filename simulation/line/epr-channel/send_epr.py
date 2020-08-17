import time
import cqc.pythonLib as cqc

#
def create_epr(node, id1, id2):
    sender = node+id1
    receiver = node+id2

    # Initialize the connection
    with cqc.CQCConnection(sender) as Alice:
        # Measure timestamp
        ts = time.time()

        # Create an EPR pair
        q = Alice.createEPR(receiver)

        # Measure qubit
        m=q.measure()

        return (sender,m,ts)
