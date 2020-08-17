import sys
from cqc.pythonLib import CQCConnection

#
def extract_path(file):
    try:
        fr = open(file,'r')
        line = fr.readline()
        route = line.split(',')
        data = [int(i) for i in route]
        fr.close()
        return data
    except IOError:
        raise

def start_classical_server(nodes):
    for id in nodes:
        node = "Node{}".format(id)
        with CQCConnection(node) as alice:
            yield alice.startClassicalServer()
            print("Starting classical server at {}".format(node))

#
def start():
    file = sys.argv[1]
    route = extract_path(file)
    start_classical_server(route)

start()
