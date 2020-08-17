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
def topology_settings(file, name, cfg_file):
    try:
        (nodes,topology) = get_topology(file)
        network = Network(name=name, nodes=nodes, topology=topology)
        return network
    except Exception:
        raise

#
def start():
    file = "./adjacency_matrix.csv"
    name = 'qn1'
    if len(sys.argv)>1:
        file = sys.argv[1]
        name = sys.argv[2]
    nw_cfg_file = "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/simulaqron/config/network.json"
    try:
        network = topology_settings(file, name, nw_cfg_file)
        network.start()
        input("To stop the network, press enter...")
    except Exception as err:
        print(err)

#
start()
