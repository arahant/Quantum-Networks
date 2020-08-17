import sys

TOTAL = 2

#
def read_metrics(file):
    data = []
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
                data.append(row)
            fr.close()
            return data
    except IOError as err:
        print(err)

#
def calculate_metrics(data):
    vote_err_bit = ["# vote err"]
    vote_err_rate = ["% vote err"]
    delay1 = ["transmission delay epr"]
    delay2 = ["transmission delay voting"]
    for x in data:
        d1 = float(x[1])-float(x[0])
        d2 = float(x[4])-float(x[3])
        va = x[2].split(".")
        vr = x[5].split(".")
        vrb = abs(int(va[0])-int(vr[0]))+abs(int(va[1])-int(vr[1]))
        vrr = float(vrb)/TOTAL
        vote_err_bit.append(vrb)
        vote_err_rate.append(vrr)
        delay1.append(d1)
        delay2.append(d2)
    return vote_err_bit,vote_err_rate,delay1,delay2

#
def print_op(x1,x2,x3,x4):
    N = len(x1)
    for i in range(N):
        print("{},{},{},{}".format(x1[i],x2[i],x3[i],x4[i]))

#
def start():
    data = read_metrics(sys.argv[1])
    x1,x2,x3,x4 = calculate_metrics(data)
    print_op(x1,x2,x3,x4)

#
start()
