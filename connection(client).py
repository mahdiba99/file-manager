import socket
import threading
import os
from Item import Item
import time

reqs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
reqs.connect(('localhost',5000))
print(reqs)

recs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
recs.connect(('localhost',6000))
print(recs)

lock = threading.Lock()

def listen(conn):
    while conn:
            print('listening...')
            req = conn.recv(1024).decode('utf-8')
            print('recieved: ',req)
            if req[:5] == 'getI ':
                path = req[5:]
                l = os.listdir(path)
                if path[-1] != '/':
                    path += '/'
                from Item import Item
                import time
                il = []
                for i in l:
                    il.append(Item(path+i,os.path.getsize(path+i),os.path.getmtime(path+i),path))
                print(il)
                ilstr = ''
                for i in il:
                    ilstr += str(i.name) + ',' + str(i.size) + ',' + str(i.date) + ',' + str(i.path) + '|||'
                conn.send(bytes(ilstr,'utf-8'))
            elif req[:4] == 'del':
                path = req[4:]
                try:
                    from phase2 import delete
                    delete(path)
                    conn.send(b'success')
                except:
                    conn.send(b'failed')
            
                
tl = threading.Thread(target = listen,args=(recs,))
tl.start()

def getitems(path,conn = reqs):
    conn.send(bytes('getI '+path,'utf-8'))
    ilstr = conn.recv(4096).decode('utf-8').split('|||')
    itemslist = []
    for i in ilstr:
        if ',' in i:
            istr = i.split(',')
            itemslist.append(Item(istr[0],float(istr[1]),time.ctime(float(istr[2])),istr[3]))
            
    return itemslist

def delete(path,conn = recs):
    conn.send(bytes('del '+path,'utf-8'))
    return conn.recv(4096).decode('utf-8')
