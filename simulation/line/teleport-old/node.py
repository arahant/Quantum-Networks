import client
import server
from cqc.pythonLib import CQCConnection

ext = "csv"
data_path = "."
data_file = "data_send"
data_file = "data_recv"

################################################################################
# CLIENT WRAPPER
#
def document_client(nd,qb,ts):
    to_print="{}'s sent qubit's measurement: {}".format(nd,qb)
    print(to_print)
    line = "{},{},{}\n".format(nd,qb,ts)
    file = open(data_path+"/"+data_file+"."+ext,"a")
    file.write(line)

# new [client] thread is spawned every time a packet is to be sent
def client_wrapper(id1,id2,riute,q1=None):
    sender = "Node"+str(id1)
    recv = "Node"+str(id2)
    with CQCConnection(sender) as alice:
        if q1 is None:
            q1 = client.create_qubit(alice)
        print("Qubit created at {}".format(sender))
        (qb,ts) = client.create_epr(alice,sender,recv)
        (b1,b2) = client.apply_locc(q1,qb)
        client.send_info(alice,recv,b1,b2)
        print("Measured bits sent to {}".format(recv))
        # document_client(sender,qb,ts)

################################################################################
# SERVER WRAPPER
#
def document_server(nd,qb,ts):
    to_print="{}'s received qubit's measurement: {}".format(nd,qb)
    print(to_print)
    line = "{},{},{}\n".format(nd,qb,ts)
    file = open("./"+data_file+"."+ext,"a")
    file.write(line)

# a new interrupt is raised every time a new packet is received
def server_wrapper(id):
    recv = "Node"+str(id)
    with CQCConnection(recv) as bob:
        (q,ts) = server.recv_epr(bob,recv)
        # (data,q) = server.get_data(q,bob,recv)
        data = bob.recvClassical()
        print("Classical data received at {}".format(recv))
        if data[0]==1:
            q.Z()
        if data[1]==1:
            q.X()

        return q
        # document_server(recv,qb,ts)

################################################################################
#
def start(route):
    # node 0 -> 1
    id1 = route.pop(0)
    id2 = route[0]
    client_wrapper(id1,id2,route,None)

    # node 1 -> 2
    id1 = route.pop(0)
    id2 = route[0]
    qb = server_wrapper(id1)
    client_wrapper(id1,id2,route,qb)

    # node 2
    data = server_wrapper(id1)
    print(data)
