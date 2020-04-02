import socket as mysoc
import sys
import select

lsListenPort = int(sys.argv[1])
ts1Hostname = sys.argv[2]
ts1ListenPort = int(sys.argv[3])
ts2Hostname = sys.argv[4]
ts2ListenPort = int(sys.argv[5])
dns = []

# create sockets
try:
    clientSocket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    print("[S]: RS socket created")
except mysoc.error as err:
    print('{} \n'.format("socket open error ", err))

try:
    ts1Socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    print("[S]: RS socket created")
except mysoc.error as err:
    print('{} \n'.format("socket open error ", err))

try:
    ts2Socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    print("[S]: RS socket created")
except mysoc.error as err:
    print('{} \n'.format("socket open error ", err))

# connect ts1Socket to ts1
ts1HostIP = mysoc.gethostbyname(ts1Hostname)
ts1SocketServerBinding = (ts1HostIP, ts1ListenPort)
ts1Socket.connect(ts1SocketServerBinding)
print("[S]: ts1Socket connected to ts1")

# connect ts1Socket to ts2
ts2HostIP = mysoc.gethostbyname(ts2Hostname)
ts2SocketServerBinding = (ts2HostIP, ts2ListenPort)
ts2Socket.connect(ts2SocketServerBinding)
print("[S]: ts2Socket connected to ts2")

clientSocketServerBinding = ('', lsListenPort)
clientSocket.bind(clientSocketServerBinding)
clientSocket.listen(1)
host = mysoc.gethostname()
print("[S]: Server host name is: ", host)
localhost_ip = (mysoc.gethostbyname(host))
print("[S]: Server IP address is  ", localhost_ip)
csockid, addr = clientSocket.accept()
print ("[S]: Got a connection request from a client at", addr)

hostname = csockid.recv(200)
while len(hostname) != 0:
    print("[S]: querying {} on ts1, ts2".format(hostname))
    ts1Socket.send(hostname)
    ts2Socket.send(hostname)
    foundMatch = select.select([ts1Socket, ts2Socket], [], [], 5)
    if foundMatch[0]:
        socketFoundMatch = foundMatch[0][0]
        if socketFoundMatch == ts1Socket:
            print("[S]: match found on ts1")
            tsResponse = ts1Socket.recv(200)
        else:
            print("[S]: match found on ts2")
            tsResponse = ts2Socket.recv(200)
        csockid.send(tsResponse)
    else:
        print("[S]: match not found")
        csockid.send("{} - Error:HOST NOT FOUND".format(hostname))
    hostname = csockid.recv(200)

clientSocket.close()
ts1Socket.close()
ts2Socket.close()
