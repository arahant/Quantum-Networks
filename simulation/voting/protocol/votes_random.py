import sys
from random import randint

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

#
def generate_random_votes(id):
    v0 = randint(0,1)
    v1 = randint(0,1)
    line = "{}:{},{}".format(id,v0,v1)
    return line

def start():
    nodes = extract_nodes(sys.argv[1])
    for i in range(1,len(nodes)):
        votes = generate_random_votes(nodes[i])
        print(votes)

start()
