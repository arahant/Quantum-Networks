import sys

#
def read_data(file):
    data = []
    try:
        with open(file) as fr:
            line = fr.readline()
            while line:
                line = fr.readline().strip()
                data.append(line.split(','))
            fr.close()
            return data
    except IOError as err:
        print(err)

#
def map_data(data):
    map = dict()
    for row in data:
        if len(row)<2:
            continue
        id = row[0]
        c = 0
        if int(row[3])==1:
            c = 1
        t = 1
        t1 = float(row[5])
        ts = t1
        td = 0
        dl = 0
        if id in map:
            val = map[id]
            c = val[2]
            t = val[3]
            t2 = val[4]
            td = val[5]
            if t2 is not 0:
                dl = abs(t1-t2)
                ts = 0
            if int(row[3])==1:
                c += 1
        map[id] = [row[1],row[2],c,t+1,ts,td+dl]
    return map

#
def reduce_data(map):
    header = ["Pair","# Err","% Err","Total","Avg Delay","Total Delay"]
    metrics = {}
    for x in map:
        n1 = map[x][0]
        n2 = map[x][1]
        id = "{}-{}".format(n1[len(n1)-1:],n2[len(n2)-1:])

        cm = map[x][2]
        cr = 0
        tm = map[x][3]
        tr = 0
        dl = map[x][5]
        tot_dl = 0
        if id in metrics:
            cr = metrics[id][0]
            tr = metrics[id][2]
            tot_dl = metrics[id][4]
        metrics[id] = [cm+cr,0,tm+tr,0.0,dl+tot_dl]

    for x in metrics:
        c = float(metrics[x][2])/2
        p = float(metrics[x][0])/c
        metrics[x][1] = round(p,3)
        avg_dl = float(metrics[x][4])/c
        metrics[x][3] = round(avg_dl,3)
        metrics[x][2] = c
    return metrics,header

#
def calculate_metrics(data):
    map = map_data(data)
    reduce,header = reduce_data(map)
    return reduce,header

#
def print_op(metrics,header):
    h = ",".join(x for x in header)
    print(h)
    for k in metrics:
        v = ",".join(str(x) for x in metrics[k])
        print("{},{}".format(k,v))

#
def start():
    data = read_data(sys.argv[1])
    metrics,header = calculate_metrics(data)
    print_op(metrics,header)

start()
