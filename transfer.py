def copy(source,destination):
    if destination[-1] != '/':
        destination += '/'
    file = source.split('/')[-1]
    s = open(source,'rb')
    d = open(destination+file,'wb')
    d.seek(0)
    s.seek(0)
    d.write(s.read())
    s.close()
    d.close()
    
def cut(source,destination):
    if destination[-1] != '/':
        destination += '/'
    file = source.split('/')[-1]
    s = open(source,'rb')
    d = open(destination+file,'wb')
    d.seek(0)
    s.seek(0)
    d.write(s.read())
    s.close()
    d.close()
    import os
    os.remove(source)
