import re
import sys

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
def rearragne_data(data):
    N = len(data)
    header = ["EPR sent","EPR recv","Cast Vote","Votes Sent","Votes recv","Recorded votes"]
    new_data = []
    # new_data.append(header)
    for row in data:
        new_row = []
        bool2a = bool2b = bool3 = bool4 = bool5 = bool6 = False
        for el in row:
            if el.startswith("2a"):
                if not bool2a:
                    bool2a = True
                    v1=re.search("\(.*\)", el).group(0)
                    v2=v1.replace("(",'')
                    v2=v2.replace(")",'')
                    new_row.append(v2)
            elif el.startswith("2b"):
                if not bool2b:
                    bool2b = True
                    v1=re.search("\(.*\)", el).group(0)
                    v2=v1.replace("(",'')
                    v2=v2.replace(")",'')
                    new_row.append(v2)
            elif el.startswith("3"):
                if not bool3:
                    bool3 = True
                    v1=re.search("\(.*\)", el).group(0)
                    v2=v1.replace("(",'')
                    v2=v2.replace(")",'')
                    new_row.append(v2)
            elif el.startswith("4"):
                if not bool4:
                    bool4 = True
                    v1=re.search("\(.*\)", el).group(0)
                    v2=v1.replace("(",'')
                    v2=v2.replace(")",'')
                    new_row.append(v2)
            elif el.startswith("5"):
                if not bool5:
                    bool5 = True
                    v1=re.search("\(.*\)", el).group(0)
                    v2=v1.replace("(",'')
                    v2=v2.replace(")",'')
                    new_row.append(v2)
            elif el.startswith("6"):
                if not bool6:
                    bool6 = True
                    v1=re.search("\(.*\)", el).group(0)
                    v2=v1.replace("(",'')
                    v2=v2.replace(")",'')
                    new_row.append(v2)
        new_data.append(new_row)
    return new_data

#
def print_op(data):
    for x in data:
        print("{},{},{},{},{},{}".format(x[0],x[1],x[2],x[3],x[4],x[5]))

#
def start():
    data = read_metrics(sys.argv[1])
    new_data = rearragne_data(data)
    print_op(new_data)

#
start()
