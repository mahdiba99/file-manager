import os
class Item:
    def __init__(self,name = None,size = None,date = None,path =None):
        self.name = name
        self.size = size
        self.path = path
        self.date = date
        self.set_icon()
    def set_icon(self):
        if os.path.isdir(self.path + "/" + self.name):
            self.icon = 'folder'
        else:
            self.icon = 'file'