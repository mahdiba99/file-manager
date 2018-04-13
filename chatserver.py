# server.py 
import socket                                         
import time

# create a socket object
serversocket = socket.socket() 

# get local machine name
host = socket.gethostname()                           

port = 5000                                       

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(5)                                           
conn, addr = serversocket.accept()

while True:
    data = conn.recv(1024).decode()  
    if data == 'q':
        conn.close()
        break
    print("Recieved :", data)
    message = input("Enter message for client : ")
    conn.send(message.encode())
    
