import sys
from cqc.pythonLib import CQCConnection

#
def start_classical_server(id):
    with CQCConnection(id) as node:
        yield node.startClassicalServer()
        print("Starting classical server at {}".format(id))

#
def start():
    node1 = "Node".format(sys.argv[1])
    node2 = "Node".format(sys.argv[2])
    start_classical_server(node1)
    start_classical_server(node2)

start()
