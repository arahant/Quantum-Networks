import sys

#
def read_metrics(file):
    original = []
    actual = []
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
                ko = int(row[0])
                ka = int(row[1])
                original.append(ko)
                actual.append(ka)
            fr.close()
            return original,actual
    except IOError as err:
        print(err)

#
def calculate_metrics(original,actual):
    err_bit = ["# bits"]
    err_percent = ["% error"]
    info_lost = []
    avg_err_bit = 0.0
    avg_err_percent = 0.0
    N = len(original)

    for i in range(N):
        o = original[i]
        a = actual[i]
        eb = o-a
        ep = float(eb)/o
        avg_err_bit += eb
        avg_err_percent += ep
        err_bit.append(eb)
        err_percent.append(ep)
    avg_err_bit = float(avg_err_bit)/N
    avg_err_percent = float(avg_err_percent)/N
    return avg_err_bit, avg_err_percent, err_bit, err_percent

#
def print_op(lst1,lst2):
    N = len(lst1)
    for x in range(N):
        print("{},{}".format(lst1[x],lst2[x]))

#
def start():
    original,actual = read_metrics(sys.argv[1])
    avg_err_bit, avg_err_percent, err_bit, err_percent = calculate_metrics(original,actual)
    # print("Average # Bit Flips: {}\nAverage Bit flip err rate: {}".format(avg_err_bit, avg_err_percent))
    print_op(err_bit,err_percent)

start()
