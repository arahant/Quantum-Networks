import sys

TAG_ST1="s1"
TAG_ST2="s2"
TAG_ST3="s3"
TAG_ST4="s4"

#
def arrange_steps(steps):
    step = {}
    for s in steps:
        if TAG_ST1 in s:
            step[TAG_ST1]=s
        elif TAG_ST2 in s:
            step[TAG_ST2]=s
        elif TAG_ST3 in s:
            step[TAG_ST3]=s
        elif TAG_ST4 in s:
            step[TAG_ST4]=s
    return step

#
def read_data(file):
    data = []
    try:
        with open(file,'r') as fr:
            line = fr.readline()
            while line:
                if not line:
                    continue
                step1 = fr.readline().strip()
                step2 = fr.readline().strip()
                step3 = fr.readline().strip()
                step4 = fr.readline().strip()
                line = step4
                if not step1 or not step2 or not step3 or not step4:
                    continue
                steps = arrange_steps([step1,step2,step3,step4])
                step = "{},{},{},{}".format(steps[TAG_ST1],steps[TAG_ST2],steps[TAG_ST3],steps[TAG_ST4])
                print(step)
                data.append(step)
            fr.close()
            return data
    except IOError as err:
        print(err)

#
def start():
    data = read_data(sys.argv[1])

#
start()
