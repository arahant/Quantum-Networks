import sys
import send_epr as sender

data_path = "."
data_file = "data_send"
ext = "csv"
node = "Node"

#
def document(nd,qb,ts):
    to_print="{}'s sent qubit's measurement: {}".format(nd,qb)
    print(to_print)
    line = "{},{},{}\n".format(nd,qb,ts)
    file = open(data_path+"/"+data_file+"."+ext,"a")
    file.write(line)

#
def start():
    (nd,qb,ts) = sender.create_epr(node,sys.argv[1],sys.argv[2])
    document(nd,qb,ts)

#
start()
