import socket as mysoc
import sys

resolvedFile = open("RESOLVED.txt", "w")

lsHostname = sys.argv[1]
lsListenPort = int(sys.argv[2])

# create socket
try:
    socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    print("[C]: socket1 created")
except mysoc.error as err:
    print('{} \n'.format("socket1 open error ", err))

# connect socket to ls
lsHostIP = mysoc.gethostbyname(lsHostname)
socketServerBinding = (lsHostIP, lsListenPort)
socket.connect(socketServerBinding)
print("[C]: socket2 connected to ls")

# query hostNames
filepath = "PROJ2-HNS.txt"
with open(filepath) as f:
    line = f.readline()
    while line:
        hostname = line.rstrip()
        print("[C]: querying {} on ls".format(hostname))
        socket.send(hostname)
        responseFromLS = socket.recv(200)
        if len(responseFromLS) == 0:
            # error
            print("[C]: ERROR - something wrong with ls server code")
            exit()
        resolvedFile.write(responseFromLS + '\n')
        print(responseFromLS)
        line = f.readline()


f.close()
resolvedFile.close()
socket.close()
