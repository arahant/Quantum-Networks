import sys
import random

node = "Node"
localhost = "localhost"
socket_limit = 9999

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
def create_nw_cfg(file,route):
    fw = open(file,'w')
    str_data = ''
    for i in range(len(route)):
        row = node+str(route[i])+','+localhost+','+str(random.randint(0,socket_limit))+'\n'
        str_data += row
    fw.write(str_data)
    fw.close()

#
def main():
    try:
        route = extract_path(sys.argv[1])
        create_nw_cfg(sys.argv[2],route)
    except IOError as err:
        print(err)

main()
