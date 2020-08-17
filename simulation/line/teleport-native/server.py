import logging
from twisted.internet.defer import inlineCallbacks
from twisted.spread import pb
from twisted.internet import reactor

#
recv = False
send_qubit = "send_qubit"
receive_qubit = "receive_qubit"
recover_teleport = "recover_teleport"

#####################################################################################################
# This will be run if the local node acts as a server on the classical communication network,
# accepting remote method calls from the other nodes.
class localNode(pb.Root):

    def __init__(self, node, classicalNet):
        self.node = node
        self.classicalNet = classicalNet

        self.virtRoot = None
        self.qReg = None

    def set_virtual_node(self, virtRoot):
        self.virtRoot = virtRoot

    def set_virtual_reg(self, qReg):
        self.qReg = qReg

    def remote_test(self):
        return "Tested!"

    @inlineCallbacks
    def remote_recover_teleport(self, a, b, virtualNum):
        ################################################################
        eprB = yield self.virtRoot.callRemote("get_virtual_ref", virtualNum)

        # Apply the desired correction info and get the qubit
        logging.debug("LOCAL %s: Correction info is a=%d, b=%d.", self.node.name, a, b)
        if b == 1:
            yield eprB.callRemote("apply_X")
        if a == 1:
            yield eprB.callRemote("apply_Z")
        q1 = eprB

        ################################################################
        # Create qubit for teleportation
        qA = yield virtRoot.callRemote("new_qubit_inreg", qReg)
        qB = yield virtRoot.callRemote("new_qubit_inreg", qReg)

        # Creating an EPR state
        yield qA.callRemote("apply_H")
        yield qA.callRemote("cnot_onto", qB)

        # Send qubit B to destination: instruct the virtual node to transfer the qubit
        recv_name = recv
        next_node = yield virtRoot.callRemote(send_qubit, qB, recv_name)

        ################################################################
        # Apply the local teleportation operations
        yield q1.callRemote("cnot_onto", qA)
        yield q1.callRemote("apply_H")

        a = yield q1.callRemote("measure")
        b = yield qA.callRemote("measure")

        # Tell destination the number of the virtual qubit so the can use it locally
        recv = classicalNet.hostDict[recv_name]
        yield recv.root.callRemote(recover_teleport, a, b, next_node)
