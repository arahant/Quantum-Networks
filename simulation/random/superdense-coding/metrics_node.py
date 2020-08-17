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
    t2 = 15
    d = 6
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
            td1 = 0
            if node1 in metrics:
                values = metrics[node1]
                vs1 = values[0]
                cs1 = values[1]
                vr1 = values[2]
                cr1 = values[3]
                td1 = values[4]
            metrics[node1] = [vs1+TR_DL_SND,cs1+1,vr1,cr1,td1+vs1+vr1+TR_DL_SND]

            vs2 = vr2 = 0
            cs2 = cr2 = 0
            td2 = 0
            if node2 in metrics:
                values = metrics[node2]
                vs2 = values[0]
                cs2 = values[1]
                vr2 = values[2]
                cr2 = values[3]
                td2 = values[4]
            metrics[node2] = [vs2,cs2,vr2+TR_DL_RCV,cr2+1,td2+vs2+vr2+TR_DL_RCV]
        except IndexError as err:
            # print(err)
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
