import sys

POS_KEY = 1
POS_ID = 0

#
def read_keys(file):
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
                k = row[POS_KEY]
                id = row[POS_ID]
                key.append(k)
            fr.close()
            return key
    except IOError as err:
        print(err)

#
def start():
    keys = read_keys(sys.argv[1])
    qkd = "1"
    qkd += "".join(keys)
    print("{}{}:{}".format(sys.argv[3],sys.argv[2],qkd))

start()
