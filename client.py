import socket, sys, threading

from time import sleep

host, port = '192.168.1.10', 8000


class recv_data :
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mysocket.connect((host, port))

    def __init__(self):
        data = self.mysocket.recv(1024)
        f = open('newfile.webm', 'wb')
        while data != bytes(''.encode()):
            #print(data)
            data = self.mysocket.recv(1024)
            f.write(data)


re = recv_data()