import socket


host = socket.gethostname()
port = 5000

mySocket = socket.socket()
mySocket.connect((host,port))
def Main(mySocket):
        while True:
                while True:
                        data = input(" -> ")

                        if data != 'q' :
                                mySocket.send(data.encode())
                        else:
                                mySocket.close()
                        break
                
                while True:
                        message = mySocket.recv(1024).decode()
                        print('Recieved :', message)
                        break   
Main(mySocket)

