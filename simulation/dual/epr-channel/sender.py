import cqc.pythonLib as cqc

# Initialize the connection
with cqc.CQCConnection("Alice") as Alice:

    # Create an EPR pair
    q = Alice.createEPR("Bob")

    # Measure qubit
    m=q.measure()
    to_print="App {}: Measurement outcome is: {}".format(Alice.name,m)
    print("+"+"-"*(len(to_print)+2)+"+")
    print("| "+to_print+" |")
    print("+"+"-"*(len(to_print)+2)+"+")
