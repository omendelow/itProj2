import socket as mysoc
import sys

rsListenPort = int(sys.argv[1])
dns = []
TSHostname = ""


def createDict():
    global TSHostname
    inputFile = open("PROJI-DNSRS.txt", "r")
    entries = inputFile.readlines()
    for i in entries:
        newEntry = i.split()
        if newEntry[2] == 'NS':
            TSHostname = newEntry[0]
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
    if len(TSHostname) == 0:
        print("ERROR - No TSHostname")
        exit()
    return TSHostname + " - NS"


def server():
    try:
        rss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: RS socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    server_binding = ('', rsListenPort)
    rss.bind(server_binding)
    rss.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid, addr = rss.accept()
    print ("[S]: Got a connection request from a client at", addr)

    hostname = csockid.recv(100)
    while len(hostname) != 0:
        csockid.send(lookUp(hostname))
        hostname = csockid.recv(100)

    rss.close()


createDict()
server()
