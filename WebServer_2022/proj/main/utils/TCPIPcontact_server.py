import socket
import time
import struct
import os

str_LANSERVER_PORT = os.environ.get('LANSERVER_PORT')
print(str_LANSERVER_PORT, type(str_LANSERVER_PORT), sep='\t')
PORT = int(str_LANSERVER_PORT)

def connect_server(sendMessage, HOST = 'host.docker.internal', PORT=PORT)->str:
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


