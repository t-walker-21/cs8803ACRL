import socket
import time
import numpy as np

UDP_IP = "localhost"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

sock2 = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

while True:
    nxtState, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "next state: ", nxtState
    resp = str(input())
    print "sending response: " , resp
    sock2.sendto(resp,(UDP_IP,5006))

    
    reward, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "reward: ", reward
    done, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "done: ", done
    #time.sleep(0.5)
    