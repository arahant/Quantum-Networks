import sys
import recv_epr as recv

data_path = "."
data_file = "data_recv"
ext = "csv"
node = "Node"

#
def document(nd,qb,ts):
    to_print="{}'s received qubit's measurement: {}".format(nd,qb)
    print(to_print)
    line = "{},{},{}\n".format(nd,qb,ts)
    file = open("./"+data_file+"."+ext,"a")
    file.write(line)

#
def start():
    (nd,qb,ts) = recv.recv_epr(node,sys.argv[1])
    document(nd,qb,ts)

#
start()
