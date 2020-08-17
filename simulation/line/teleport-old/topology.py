from simulaqron.network import Network
# import alice as alice
# import bob as bob

def topology_settings():
    nodes = ["Node0","Node1", "Node2", "Node3", "Node4", "Node5", "Node6", "Node7", "Node8", "Node9"]
    topology = {
        "Node0": ["Node1"],
        "Node1": ["Node0","Node2"],
        "Node2": ["Node1", "Node3"],
        "Node3": ["Node2", "Node4"],
        "Node4": ["Node3", "Node5"],
        "Node5": ["Node4", "Node6"],
        "Node6": ["Node5", "Node7"],
        "Node7": ["Node6", "Node8"],
        "Node8": ["Node7", "Node9"],
        "Node9": ["Node8"]
    }
    # config_file = "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/simulaqron/config/network.json"
    network = Network(nodes=nodes, topology=topology)
    return network

def create_topology():
    network = topology_settings()
    network.start()
    input("To stop the network, press enter...")

def start():
    create_topology()

start()
