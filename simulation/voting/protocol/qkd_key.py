import sys

POS_KEY = 1
POS_ID = 0

#
def read_key(file):
    key = []
    try:
        with open(file,'r') as fr:
            line = fr.readline()
            while line:
                line = line = fr.readline()
                line = line.strip()
                if not line:
                    continue
                row = line.split(',')
                if len(row)==0:
                    continue
                k = int(row[POS_KEY])
                id = row[POS_ID]
                key.append(k)
            fr.close()
            return key
    except IOError as err:
        print(err)

#
def qkd_key(key_gov,key_ctz):
    line = '1'
    size = 0
    for i in range(len(key_gov)):
        if key_gov[i]==key_ctz[i]:
            line += "{}".format(key_gov[i])
            size += 1
    return (line,size)

#
def start():
    key_ctz = read_key(sys.argv[1])
    key_gov = read_key(sys.argv[2])
    (line,size) = qkd_key(key_gov,key_ctz)
    print("{}{}:{}\n{}".format(sys.argv[4],sys.argv[3],line,size))

start()
