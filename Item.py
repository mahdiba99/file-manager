class Item:
    def __init__(self,name,size,path):
        self.name = name
        self.size = size
        self.path = path

    def copy(self,path, destination):
        if destination[-1] != '/':
            destination += '/'
        file = path.split('/')[-1]
        s = open(path, 'rb')
        d = open(destination + file, 'wb')
        d.seek(0)
        s.seek(0)
        d.write(s.read())
        s.close()
        d.close()

    def cut(self,path, destination):
        if destination[-1] != '/':
            destination += '/'
        file = path.split('/')[-1]
        s = open(path, 'rb')
        d = open(destination + file, 'wb')
        d.seek(0)
        s.seek(0)
        d.write(s.read())
        s.close()
        d.close()
        import os
        os.remove(path)