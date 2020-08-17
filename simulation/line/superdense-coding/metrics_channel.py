import sys

#
def read_data(file):
    data = []
    try:
        with open(file,'r') as fr:
            line = fr.readline().strip()
            data.append(line)
            while line:
                line = fr.readline().strip()
                if not line:
                    continue
                data.append(line)
            fr.close()
            return data
    except IOError as err:
        print(err)

#
def calculate_metrics(data):
    headers = ["Channel","1st bit err","2nd bit err","Total transmissions"]
    metrics = {}
    # 1. Transmission delay send (TR_DL_SND) = TS_BIT_SND - TS_EPR_SND
    # 2. Transmission delay recv (TR_DL_RCV) = TS_BIT_RCV - TS_EPR_RCV
    # 3. Transmission delay Node = TR_DL_SND + TR_DL_RCV
    for r in data:
        try:
            x = r.split(',')
            n1 = x[0][len(x[0])-1:]
            n2 = x[1][len(x[1])-1:]
            key = "{}-{}".format(n1,n2)

            b0s = int(x[10])
            b1s = int(x[11])
            b0r = int(x[22])
            b1r = int(x[23])

            b0e = abs(b0s-b0r)
            b1e = abs(b1s-b1r)
            b0c = b1c = tc = 0

            if key in metrics:
                values = metrics[key]
                b0c = values[0]
                b1c = values[1]
                tc = values[2]

            metrics[key] = [b0c+b0e,b1c+b1e,tc+1]
        except IndexError as err:
            continue
    return metrics,headers

#
def print_op(metrics,headers):
    h = ",".join(x for x in headers)
    print(h)
    for k in metrics.keys():
        v = ",".join(str(x) for x in metrics[k])
        r = "{},{}".format(k,v)
        print(r)

#
def start():
    data = read_data(sys.argv[1])
    metrics,headers = calculate_metrics(data)
    print_op(metrics,headers)

#
start()
