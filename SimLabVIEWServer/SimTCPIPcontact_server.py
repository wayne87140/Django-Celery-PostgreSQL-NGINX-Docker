import socket
import time
import struct
import os


def connect_server(sendMessage, HOST = '127.0.0.1', PORT=8824)->str:
    # connect to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    # create connection
    client.send(sendMessage)
    time.sleep(0.8)
    # decode binary string to list
    len_receiveMessage = struct.unpack('!i', client.recv(4))[0]
    receiveMessage = client.recv(len_receiveMessage)
       
    client.close()
    
    return receiveMessage


