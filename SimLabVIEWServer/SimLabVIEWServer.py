import socket
# import struct
import createMSG


HOST = '127.0.0.1'
PORT = 8824
cmd_device_status = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x02F0'
cmd_user_info =  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x02F1'

            
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()

    while True:
        try:
            conn, addr = server.accept()
            
            receive_len = int.from_bytes(conn.recv(4), 'big')
            receiveMsg = conn.recv(receive_len)
            
            if receiveMsg == cmd_device_status:
                conn.sendall(createMSG.device_status())
            
            if receiveMsg == cmd_user_info:
                conn.sendall(createMSG.user_info())
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
            break
    server.close()

# # Solution for execute once
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
#     server.bind((HOST, PORT))
#     server.listen()
#     conn, addr = server.accept()

#     receive_len = int.from_bytes(conn.recv(4), 'big')
#     receiveMsg = conn.recv(receive_len)
    
#     if receiveMsg == cmd_device_status:
#         conn.sendall(createMSG.device_status())
    
#     if receiveMsg == cmd_user_info:
#         conn.sendall(createMSG.user_info())