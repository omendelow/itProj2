import socket as mysoc
import sys

tsListenPort = int(sys.argv[1])
dns = []


def createDict():
    inputFile = open("PROJ2-DNSTS1.txt", "r")
    entries = inputFile.readlines()
    for i in entries:
        newEntry = i.split()
        dns.append(newEntry)
    inputFile.close()


def printDict():
    for entry in dns:
        print(entry)


def lookUp(hostname):
    print("[S]: looking up hostname: " + hostname)
    for i in dns:
        if hostname.lower() == i[0].lower():
            print("[S]: match found")
            return i[0] + " " + i[1] + " " + i[2]
    print("[S]: match not found")
    return ""


def server():
    try:
        tss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: TS socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    server_binding = ('', tsListenPort)
    tss.bind(server_binding)
    tss.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid, addr = tss.accept()
    print ("[S]: Got a connection request from a client at", addr)

    hostname = csockid.recv(200)
    while len(hostname) != 0:
        searchResult = lookUp(hostname)
        if len(searchResult) != 0:
            csockid.send(searchResult)
        hostname = csockid.recv(200)
    tss.close()


createDict()
server()
