import client
import server
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor

#
node = "Node"
localhost = "localhost"
socket_limit = 9999
recv = False

# function calls
send_qubit = "send_qubit"
receive_qubit = "receive_qubit"
recover_teleport = "recover_teleport"

#
def set_recv(re):
    recv = re

#####################################################################################################
# This will be run on the local node if all communication links are set up (to the virtual node
# quantum backend, as well as the nodes in the classical communication network),
# and the local classical communication server is running (if applicable).
@inlineCallbacks
def runClientNode(qReg, virtRoot, myName, classicalNet):
    ################################################################
    q1 = yield virtRoot.callRemote("new_qubit_inreg", qReg)
    # yield q1.callRemote("apply_X")
    yield q1.callRemote("apply_H")

    ################################################################
    # Create qubits for teleportation
    qA = yield virtRoot.callRemote("new_qubit_inreg", qReg)
    qB = yield virtRoot.callRemote("new_qubit_inreg", qReg)

    # Creating an EPR state
    yield qA.callRemote("apply_H")
    yield qA.callRemote("cnot_onto", qB)

    # Send qubit B to destination: instruct the virtual node to transfer the qubit
    recv_name = recv
    next_node = yield virtRoot.callRemote(send_qubit, qB, recv_name)
    print("Entanglement channel established between {}{}".format(myName,recv))

    ################################################################
    # Apply the local teleportation operations
    yield q1.callRemote("cnot_onto", qA)
    yield q1.callRemote("apply_H")

    a = yield q1.callRemote("measure")
    b = yield qA.callRemote("measure")

    # Tell destination the number of the virtual qubit so the can use it locally
    recv = classicalNet.hostDict[recv_name]
    yield recv.root.callRemote(recover_teleport, a, b, next_node)
    print("Qubits teleported to {}{}".format(recv))

    # reactor.stop()
