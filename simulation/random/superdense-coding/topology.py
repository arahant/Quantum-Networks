import sys
import numpy as np
from simulaqron.network import Network

#
def adjacency_matrix(file):
    data = []
    c=0
    try:
        file = open(file,'r')
        line = file.readline()
        row = line.split(',')
        row_int = [int(i) for i in row]
        data.append(row_int)
        while line:
            line = file.readline()
            if not line:
                continue;
            row = line.split(',')
            row_int = [int(i) for i in row]
            data.append(row_int)
        file.close()
        return data
    except IOError:
        raise

#
def validate_matrix(matrix):
    m = np.array(matrix)
    mT = m.transpose()
    if (m == mT).all() and (all (len(row) == len(m) for row in m)):
        return True
    else:
        raise SyntaxError('Invalid adjacency matrix')

#
def construct_topology(matrix):
    # Nodes list
    node = "Node"
    N = len(matrix)
    nodes = [(node+str(i)) for i in range(N)]

    # Topology
    topology = {}
    for i in range(N):
        neighbours = []
        for j in range(len(matrix[i])):
            if i!=j and matrix[i][j]>0:
                neighbours.append(node+str(j))
        topology[node+str(i)] = neighbours

    return (nodes,topology)

#
def get_topology(data_file):
    try:
        # adjacency matrix
        matrix = adjacency_matrix(data_file)
        validate_matrix(matrix)

        # constructing topology
        (nodes,topology) = construct_topology(matrix)
        return (nodes,topology)
    except IOError:
        raise
    except SyntaxError:
        raise

#
def start():
    file = sys.argv[1]
    try:
        (nodes,topology) = get_topology(file)
        network = Network(nodes=nodes, topology=topology, force=True)
        network.start()
        input("SimulaQron has started. To stop the network, press enter...")
    except Exception:
        raise

#
if __name__ == '__main__':
    start()
