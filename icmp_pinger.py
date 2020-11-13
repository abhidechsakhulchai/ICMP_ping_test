from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

def checksum(str):
    str = bytearray(str)
    csum = 0
    countTo = (len(str) // 2) * 2

    count = 0
    while count < countTo:
        thisVal = (str)[count+1] * 256 + (str)[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(str):
        csum = csum + (str)[-1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    andswer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def recieveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."
        timeRecieved = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        icmph = recPacket[20:28]
        type, code, mychecksum, pID, sq = struct.unpack("bbHHh", icmph)

        print ("The header received in the ICMP reply is ",type, code, checksum, pID, sq)
        if pID == ID:
            bytesinDbl = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesinDbl])[0]
            rtt= timeRecieved - timeSent

        print ("RTT is : ")
        return rtt

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out"

def sendOnePing(mySocket, destAddr, ID):
    myChecksum = 0
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0 , myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    myChecksum = checksum(header + data)

    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")

    mySocket = socket(AF_INET, SOCK_DGRAM)

    myID = os.getpid() & 0xFFFF
    sendOnePing(mySocket, destAddr, myID)
    delay = recieveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay

def ping(host, timeout=1):
    dest = gethostbyname(host)
    print ("Pinging" + dest + "using Python:")
    print ("")
    while 1:
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)
    return delay

ping("www.sjsu.edu")