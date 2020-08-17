#
def read_data(path,file):
    data = []
    try:
        fr = open(path+"/"+file)
        line = fr.readline()
        heading = line.split(',')
        while line:
            line = fr.readline()
            row = line.split(',')
            ts = float(row[0])
            qb = int(row[1])
            val = [ts,qb]
            data.append(val)
        fr.close()
    finally:
        return data

#
def calculate_avg(data_alice,data_bob):
    thr = []
    n = len(data_alice)
    for i in range(0,n):
        ts1 = data_alice[i][0]
        ts2 = data_bob[i][0]
        ts = float(ts2-ts1)
        thr.append(ts)

    avg = sum(thr)/n
    return avg

def calculate_err(data_alice,data_bob):
    err = 0
    n = len(data_alice)
    for i in range(0,n):
        qb1 = data_alice[i][1]
        qb2 = data_bob[i][1]
        if qb1!=qb2:
            err += 1
    return err

#
def metrics(data_alice,data_bob):
    avg = calculate_avg(data_alice,data_bob)
    errno = calculate_err(data_alice,data_bob)
    err = errno/len(data_alice)
    return (avg,err)

#
def start():
    data_path1 = "."
    data_file1 = "alice_data.csv"
    data_alice = read_data(data_path1,data_file1)

    data_path2 = "."
    data_file2 = "bob_data.csv"
    data_bob = read_data(data_path2,data_file2)

    (avg,err) = metrics(data_alice,data_bob)
    print("Avg time for 1 qubit: {}".format(avg))
    print("Error percentage: {}".format(err))

#
start()
