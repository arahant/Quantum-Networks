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
    headers = ["Node","Sending Delay","# sent","Receiving Delay","# received","Total delay"]
    t1 = 3
    t2 = 11
    d = 4
    metrics = {}
    # 1. Transmission delay send (TR_DL_SND) = TS_BIT_SND - TS_EPR_SND
    # 2. Transmission delay recv (TR_DL_RCV) = TS_BIT_RCV - TS_EPR_RCV
    # 3. Transmission delay Node = TR_DL_SND + TR_DL_RCV
    for r in data:
        try:
            x = r.split(',')

            TR_DL_SND = float(x[t1+d])-float(x[t1])
            TR_DL_RCV = float(x[t2+d])-float(x[t2])
            node1 = x[0]
            node2 = x[1]

            vs1 = vr1 = 0
            cs1 = cr1 = 0
            if node1 in metrics:
                values = metrics[node1]
                vs1 = values[0]
                cs1 = values[1]
                vr1 = values[2]
                cr1 = values[3]
            metrics[node1] = [vs1+TR_DL_SND,cs1+1,vr1,cr1]

            vs2 = vr2 = 0
            cs2 = cr2 = 0
            if node2 in metrics:
                values = metrics[node2]
                vs2 = values[0]
                cs2 = values[1]
                vr2 = values[2]
                cr2 = values[3]
            metrics[node2] = [vs2,cs2,vr2+TR_DL_RCV,cr2+1]
        except IndexError as err:
            # print(err)
            continue
    return metrics,headers

#
def print_op(metrics,headers):
    print("{},{},{},{},{},{}".format(headers[0],headers[1],headers[2],headers[3],headers[4],headers[5]))
    for k in metrics.keys():
        print("{},{},{},{},{},{}".format(k,metrics[k][0],metrics[k][1],metrics[k][2],metrics[k][3],metrics[k][0]+metrics[k][2]))

#
def start():
    data = read_data(sys.argv[1])
    metrics,headers = calculate_metrics(data)
    print_op(metrics,headers)

#
start()
