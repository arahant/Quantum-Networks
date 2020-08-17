import sys
import logging

import client
import server

from simulaqron.local.setup import setup_local
from simulaqron.general.hostConfig import socketsConfig
from simulaqron.settings import simulaqron_settings

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

#
def get_next_node(route,id):
    node = "Node"
    if id<(len(route)-1):
        return node+str(route[id+1])
    else:
        return False

#
def main():
    try:
        node = "Node"
        classicalFile = sys.argv[2]
        network_file = simulaqron_settings.network_config_file
        virtualNet = socketsConfig(network_file)
        classicalNet = socketsConfig(classicalFile)
        route = extract_path(sys.argv[1])
        local_nodes = []

        for id in range(len(route)):
            myName = node+str(route[id])
            lNode = None
            if myName in classicalNet.hostDict:
                lNode = server.localNode(classicalNet.hostDict[myName], classicalNet)
            local_nodes.append(lNode)

        for id in range(len(route)):
            myName = node+str(route[id])
            recv = get_next_node(route,id)
            lNode = local_nodes[id]
            print(lNode)
            if recv is not False:
                client.set_recv(recv)
                setup_local(myName, virtualNet, classicalNet, lNode, client.runClientNode)
            else:
                print("Retrieving teleported qubit: {}".format(myName))

    except IOError as err:
        print(err)

#
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", level=logging.DEBUG)
main()
