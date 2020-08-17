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
            nd = row[0]
            qb = int(row[1])
            ts = float(row[2])
            val = [nd,qb,ts]
            data.append(val)
        fr.close()
    finally:
        return data

#
def merge_data(data_send,data_recv,data_path,data_file):
    n = len(data_send)
    for i in range(n):
        n1 = data_send[i][0]
        q1 = data_send[i][1]
        t1 = data_send[i][2]
        n2 = data_recv[i][0]
        q2 = data_recv[i][1]
        t2 = data_recv[i][2]
        line = "{},{},{},{},{},{},{},{},{}\n".format(n1,n2,q1,q2,t1,t2,(t2-t1),float(1)/(t2-t1),abs(q1-q2))
        file = open(data_path+"/"+data_file,"a")
        file.write(line)

#
def start():
    data_path1 = "."
    data_file1 = "data_send.csv"
    data_send = read_data(data_path1,data_file1)

    data_path2 = "."
    data_file2 = "data_recv.csv"
    data_recv = read_data(data_path2,data_file2)

    data_path3 = "."
    data_file3 = "data_nw.csv"
    merge_data(data_send,data_recv,data_path3,data_file3)

    print("Data updated successfully!")
#
start()
