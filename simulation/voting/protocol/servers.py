import sys
from cqc.pythonLib import CQCConnection

#
def extract_nodes(file):
    nodes = []
    try:
        with open(file,'r') as fr:
            line = fr.readline()
            line = line.strip()
            nodes = [int(n) for n in line.split(',')]
            fr.close()
            return nodes
    except IOError as err:
        print(err)

# start classical servers of nodes
def start_classical_server(id):
    with CQCConnection(id) as node:
        yield node.startClassicalServer()

#
def start():
    nodes = extract_nodes(sys.argv[1])
    for i in nodes:
        node = "Node{}".format(i)
        start_classical_server(node)

start()
