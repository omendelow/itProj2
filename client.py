import socket as mysoc
import sys

resolvedFile = open("RESOLVED.txt", "w")

rsHostName = sys.argv[1]
tsHostName = ""
rsListenPort = int(sys.argv[2])
tsListenPort = int(sys.argv[3])

try:
    socket1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    print("[C]: socket1 created")
except mysoc.error as err:
    print('{} \n'.format("socket1 open error ", err))

try:
    socket2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    print("[C]: socket2 created")
except mysoc.error as err:
    print('{} \n'.format("socket2 open error ", err))

# connect socket 2
rsHostIP = mysoc.gethostbyname(rsHostName)
socket2ServerBinding = (rsHostIP, rsListenPort)
socket2.connect(socket2ServerBinding)
print("[C]: socket2 connected to rs")

socket1Connected = False


# query hostNames
filepath = "PROJI-HNS.txt"
with open(filepath) as f:
    line = f.readline()
    while line:
        hostname = line.rstrip()
        print("[C]: querying {} on rs".format(hostname))
        socket2.send(hostname)
        responseFromRS = socket2.recv(100)
        if len(responseFromRS) == 0:
            # error
            print("[C]: ERROR - something wrong with rs server code")
            exit()
        if responseFromRS[-1] == 'A':
            resolvedFile.write(responseFromRS + '\n')
        else:
            if not socket1Connected:
                # connect socket 1
                tsHostName = responseFromRS.split()[0]
                # using tsHostName, obtain ts server IP address
                tsHostIP = mysoc.gethostbyname(tsHostName)
                socket1ServerBinding = (tsHostIP, tsListenPort)
                socket1.connect(socket1ServerBinding)
                print("[C]: socket1 connected to ts")
                socket1Connected = True
            print("[C]: querying {} on ts".format(hostname))
            socket1.send(hostname)
            responseFromTS = socket1.recv(100)
            if len(responseFromTS) == 0:
                # error
                print("[C]: ERROR - something wrong with ts server code")
                exit()
            resolvedFile.write(responseFromTS + '\n')

        line = f.readline()


f.close()
resolvedFile.close()
socket1.close()
socket2.close()
