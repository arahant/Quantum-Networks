import cqc.pythonLib as cqc

# Initialize the connection
with cqc.CQCConnection("Bob") as Bob:

    # Receive qubit
    q=Bob.recvEPR()

    # Measure qubit
    m=q.measure()
    to_print="App {}: Measurement outcome is: {}".format(Bob.name,m)
    print("+"+"-"*(len(to_print)+2)+"+")
    print("| "+to_print+" |")
    print("+"+"-"*(len(to_print)+2)+"+")
