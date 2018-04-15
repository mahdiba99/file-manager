from PyQt5 import QtCore, QtGui, QtWidgets
import os, time, shutil,string,socket,threading
from dialog import Ui_Dialog
from Item import Item

global addr,pc


class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)
        self.clipboard = "Nothing yet"
        self.fileIcon = QtGui.QIcon(QtGui.QPixmap("icons/file.png"))
        self.folderIcon = QtGui.QIcon(QtGui.QPixmap("icons/folder.png"))
        global addr

    def getItems(self, path):
        if path:
            os.chdir(path)
            itemlist = os.listdir()
            items = []
            for item in itemlist:
                curr_item = Item(item, os.path.getsize(path + '/' + item), time.ctime(os.path.getmtime(path + '/' + item)),
                                path)
                items.append(curr_item)
            return items
        else:
            return []

    def set_table(self,items = []):
        if addr == '' or addr != None or addr == 'other ':
            if len(items) != 0 or addr == '':
                for i in range(len(items)):
                    self.setRowCount(len(items))
                    self.setColumnCount(3)
                    self.setHorizontalHeaderLabels(("Name", "Date Modified", "Size"))
                    self.autoFillBackground()
                    icon3 = self.fileIcon

                    if items[i].icon == 'folder':
                        icon3 = self.folderIcon
                    self.setItem(i, 0, QtWidgets.QTableWidgetItem(icon3, items[i].name))
                    self.setItem(i, 1, QtWidgets.QTableWidgetItem(items[i].date))
                    if icon3 == self.folderIcon:
                        self.setItem(i, 2, QtWidgets.QTableWidgetItem("--"))
                    else:
                        if items[i].size // 1000000000 != 0:
                            size = str(round(items[i].size / 1000000000, 2)) + " GB"
                        elif items[i].size // 1000000 != 0:
                            size = str(round(items[i].size / 1000000, 2)) + " MB"
                        elif items[i].size // 1000 != 0:
                            size = str(round(items[i].size / 1000, 2)) + " KB"
                        else:
                            size = str(items[i].size) + " B"
                        self.setItem(i, 2, QtWidgets.QTableWidgetItem(size))
                self.resizeColumnsToContents()
            else:

                self.setRowCount(len(items))
                self.setColumnCount(3)
                self.setHorizontalHeaderLabels(("Name", "Date Modified", "Size"))
                self.autoFillBackground()
        else:
            self.setRowCount(2)
            self.setColumnCount(3)
            self.setHorizontalHeaderLabels(("Name", "Date Modified", "Size"))
            self.autoFillBackground()
            items.append(Item('This PC', '--', '--',''))
            items.append(Item('Other PC', '--', '--',''))
            for i in range(len(items)):
                icon3 = self.folderIcon
                self.setItem(i, 0, QtWidgets.QTableWidgetItem(icon3, items[i].name))
                self.setItem(i, 1, QtWidgets.QTableWidgetItem(items[i].date))
                self.setItem(i, 2, QtWidgets.QTableWidgetItem(items[i].size))
            self.resizeColumnsToContents()

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        CopyAction = menu.addAction("Copy")
        CutAction = menu.addAction("Cut")
        delAction = menu.addAction("Delete")
        newAction = menu.addAction("NewFolder")
        pasteAction = menu.addAction("Paste")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == delAction:
            if addr:
                remove_path = addr + '/' + str(self.item(self.currentRow(), self.currentColumn()).text())
                delete(remove_path, None, self)
        if action == CopyAction:
            self.clipboard = [
                addr.replace('\\', '/', -1) + '/' + str(self.item(self.currentRow(), self.currentColumn()).text()),
                False]
        if action == CutAction:
            self.clipboard = [
                addr.replace('\\', '/', -1) + '/' + str(self.item(self.currentRow(), self.currentColumn()).text()),
                True]
        if action == newAction:
            newfolder(addr, None, self)
        if action == pasteAction:
            paste(self)
def paste(table):
    try:
        if table.clipboard == 'Nothing yet':
            pass
        else:
            if table.clipboard[1] == True:
                copy(table.clipboard[0], addr, table)
                delete(table.clipboard[0], None, table)
                table.clipboard = 'Nothing yet'

            else:
                copy(table.clipboard[0], addr, table)
    except:
        pass


def copy(source, destination, table=None):
    destination += source[::-1][:source[::-1].find("/") + 1][::-1]
    try:
        if not os.path.exists(destination):
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copyfile(source, destination)
        else:
            destination += '(copy)'
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copyfile(source, destination)
    except :
        pass
    try:
        table.set_table(table.getItems(addr))
    except:
        pass

def delete(address, ui=None, table=None):
    try:
        address = address.replace('\\', '/', -1)
        if os.path.isdir(address):
            shutil.rmtree(address)
        else:
            os.remove(address)

    except:
        pass
    try:
        ui.TableWidget.set_table(ui.TableWidget.getItems(addr))
    except:
        try:
            table.set_table(table.getItems(addr))
        except:
            pass


def newfolder(address, ui=None, table=None):
        try:
            os.makedirs(address + "/" + "NewFolder")
        except:
            pass
        try:
            ui.TableWidget.set_table(ui.TableWidget.getItems(addr))
        except:
            try:
                table.set_table(table.getItems(addr))
            except:
                pass
def tgetfile(opath,loc):
    try:
        tg = threading.Thread(target = getfile , args = (opath,loc))
        tg.start()
    except:
        pass

class Ui_MainWindow():
    def __init__(self):
        MainWindow = QtWidgets.QMainWindow()
        self.itemlocation = addr
        self.setupUi(MainWindow)
        MainWindow.show()
        self.lineEdit.setText(addr)
        self.fileIcon = QtGui.QIcon(QtGui.QPixmap("icons/file.png"))
        self.folderIcon = QtGui.QIcon(QtGui.QPixmap("icons/folder.png"))
        self.TableWidget.set_table(self.TableWidget.getItems(addr))
        root = self.fileSystemModel.setRootPath(addr)
        self.TreeView.setModel(self.fileSystemModel)
        self.TreeView.setRootIndex(root)

        sys.exit(app.exec_())

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(800, 650)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/مدارک/picture-24048-1508053366.jpg"), QtGui.QIcon.Normal,
                       QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAccessibleDescription("")
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setWindowFilePath("")
        MainWindow.setInputMethodHints(QtCore.Qt.ImhNone)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TreeView = QtWidgets.QTreeView(self.centralwidget)
        self.TreeView.setGeometry(QtCore.QRect(10, 80, 251, 501))
        self.TreeView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.TreeView.setObjectName("TreeView")
        ##################################TReee View###################################################
        self.fileSystemModel = QtWidgets.QFileSystemModel(self.TreeView)
        self.fileSystemModel.setReadOnly(False)

        Layout = QtWidgets.QVBoxLayout()
        Layout.addWidget(self.TreeView)
        ##########################################################################################
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 41, 28))
        self.pushButton.setText("")
        ###############################################################
        self.pushButton.clicked.connect(self.up)
        ###############################################################
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/left2.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton.setIcon(icon1)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 10, 41, 28))
        self.pushButton_2.setText("")
        ###############################################################
        self.pushButton_2.clicked.connect(self.back)
        ###############################################################
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/rightpng.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 50, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Nazanin")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(660, 10, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Ravie")
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        ###############################################################
        self.pushButton_3.clicked.connect(self.browse)
        ###############################################################

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(140, 10, 511, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.TableWidget = TableWidget(self.centralwidget)
        self.TableWidget.setGeometry(QtCore.QRect(270, 80, 511, 501))
        self.TableWidget.setObjectName("TableView")
        self.TableWidget.doubleClicked.connect(self.doubleClicked)
        self.TableWidget.clicked.connect(self.itemclicked)

        ####################tableview###################################
        self.fileSystemModel = QtWidgets.QFileSystemModel(self.TableWidget)
        self.fileSystemModel.setReadOnly(False)
        root = self.fileSystemModel.setRootPath("/")
        self.TableWidget.setRootIndex(root)

        Layout = QtWidgets.QVBoxLayout()
        Layout.addWidget(self.TableWidget)
        ####################################################################
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.deletebutton = QtWidgets.QPushButton(self.centralwidget)
        self.deletebutton.setGeometry(QtCore.QRect(290, 590, 93, 28))
        self.deletebutton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.deletebutton.setIcon(icon3)
        self.deletebutton.setIconSize(QtCore.QSize(30, 30))
        self.deletebutton.setFlat(True)
        self.deletebutton.setObjectName("deletebutton")
        self.deletebutton.clicked.connect(lambda: delete(self.itemlocation, self))
        self.newbutton = QtWidgets.QPushButton(self.centralwidget)
        self.newbutton.setGeometry(QtCore.QRect(390, 590, 93, 28))
        self.newbutton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/icons/newfolder.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.newbutton.setIcon(icon4)
        self.newbutton.setIconSize(QtCore.QSize(30, 30))
        self.newbutton.setFlat(True)
        self.newbutton.setObjectName("newbutton")
        self.newbutton.clicked.connect(lambda: newfolder(addr, self))
        self.copybutton = QtWidgets.QPushButton(self.centralwidget)
        self.copybutton.setGeometry(QtCore.QRect(490, 590, 93, 28))
        self.copybutton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/newPrefix/icons/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.copybutton.setIcon(icon5)
        self.copybutton.setIconSize(QtCore.QSize(30, 30))
        self.copybutton.setFlat(True)
        self.copybutton.setObjectName("copybutton")
        ###################################################################
        self.copybutton.clicked.connect(lambda: self.clipboard(str(self.itemlocation), False))
        self.cutbutton = QtWidgets.QPushButton(self.centralwidget)
        self.cutbutton.setGeometry(QtCore.QRect(585, 590, 93, 28))
        self.cutbutton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/newPrefix/icons/Cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cutbutton.setIcon(icon6)
        self.cutbutton.setIconSize(QtCore.QSize(30, 30))
        self.cutbutton.setFlat(True)
        self.cutbutton.setObjectName("cutbutton")
        self.cutbutton.clicked.connect(lambda: self.clipboard(str(self.itemlocation), True))
        self.downbutton = QtWidgets.QPushButton(self.centralwidget)
        self.downbutton.setGeometry(QtCore.QRect(670, 590, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Titr")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.downbutton.setFont(font)
        self.downbutton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/newPrefix/icons/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.downbutton.setIcon(icon6)
        self.downbutton.setIconSize(QtCore.QSize(30, 30))
        self.downbutton.setFlat(True)
        self.downbutton.setObjectName("downbutton")
        self.downbutton.clicked.connect(lambda:tgetfile(str(self.itemlocation),'c:/downloads'))
        
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def itemclicked(self, item):
        if item.column() == 0 and addr:
            self.itemlocation = addr + '/' + str(item.data())
        else:
            self.itemlocation = None

    def doubleClicked(self, item):
        global addr,pc
        if type(addr) == type(''):
            addr = addr.replace('//','/',-1)
        if item.column() == 0:
            if addr == '' or addr:
                if addr == 'other ':
                    addr += str(item.data())+'/'
                    self.lineEdit.setText(addr)
                    self.browse()
                elif addr[:6] == 'other ':
                    if addr[-1] != '/' or addr[-1] != '\\':
                        addr += '/'
                    addr += str(item.data())
                    self.lineEdit.setText(addr)
                    self.browse()
                elif  addr and os.path.isdir(addr + "/" + str(item.data())):
                    if addr[-1]=='/' or addr[-1]=='\\':
                        addr += str(item.data())
                    else:
                        addr +='/'+str(item.data())
                    self.lineEdit.setText(addr)
                    self.browse()
                elif addr=='':
                    addr = str(item.data())+'/'
                    self.lineEdit.setText(addr)
                    self.browse()
                else:
                    preaddr = addr
                    if addr[-1]=='/' or addr[-1]=='\\':
                        addr += str(item.data())
                    else:
                        addr +='/'+str(item.data())
                    self.browse()

                    addr = preaddr
                    self.lineEdit.setText(addr)
            elif addr == None:

                if str(item.data()) == 'This PC':
                    addr = ''
                    self.browse()
                elif str(item.data()) == 'Other PC':
                    global recs
                    try:
                        print('try')
                        print(recs)
                    except:
                        import req
                        dialog = QtWidgets.QDialog()
                        dialog.ui = req.Ui_Dialog()
                        dialog.ui.setupUi(dialog)
                        result = dialog.exec_()
                        dialog.show()
                        if result == dialog.Accepted:
                            print('server up and running')

                            reqs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                            reqs.connect(('localhost',5000))


                            recs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                            recs.connect(('localhost',6000))


                            print('connected')

                            def listen(conn):
                                while conn:
                                    try:

                                        req = conn.recv(1024).decode('utf-8')
                                        print('recieved: ',req)
                                        if req[:5] == 'getI ':
                                            if req == 'getI ':
                                                path = ''
                                                l=[]
                                                b = 'abcdefghijklmnopqrstuvwxyz'
                                                for i in b:
                                                    if os.path.exists(i+':/'):
                                                        l.append(i+':/')
                                            else:
                                                path = req[5:]
                                                l = os.listdir(path)
                                                if path[-1] != '/':
                                                    path += '/'
                                            from Item import Item
                                            import time
                                            il = []
                                            for i in l:
                                                il.append(Item(i,os.path.getsize(path+i),os.path.getmtime(path+i),path))
                                            ilstr = ''
                                            for i in il:
                                                ilstr += str(i.name) + ',' + str(i.size) + ',' + str(i.date) + ',' + str(i.path) + '|||'
                                            conn.send(bytes(ilstr,'utf-8'))
                                        elif req[:4] == 'del':
                                            path = req[4:]
                                            try:

                                                delete(path)
                                                conn.send(b'success')
                                            except:
                                                conn.send(b'failed')
                                        elif req[:7] == 'giveme ':
                                            path = req[7:]
                                            file = open(path,'rb')
                                            file.seek(0)
                                            conn.send(file.read())
                                            conn.send(bytes('EOF','utf-8'))
                                            file.close()
                                        elif req == 'close':
                                            conn.close()
                                    except:
                                        pass
                            try:
                                tl = threading.Thread(target = listen,args=(recs,))
                                tl.start()
                            except:
                                pass
                            global ogetitems,odelete,getfile
                            def ogetitems(path,conn = reqs):
                                print('sg')
                                path = path.replace('//','/',-1)
                                #print(path)
                                conn.send(bytes('getI '+path,'utf-8'))
                                ilstr = conn.recv(4096).decode('utf-8').split('|||')
                                #print(ilstr)
                                itemslist = []
                                for i in ilstr:
                                    if ',' in i:
                                        istr = i.split(',')
                                        #print(istr)
                                        itemslist.append(Item(istr[0],float(istr[1]),time.ctime(float(istr[2])),istr[3]))
                                #print(itemslist)
                                return itemslist

                            def odelete(path,conn = reqs):
                                conn.send(bytes('del '+path,'utf-8'))
                                return conn.recv(4096).decode('utf-8')

                            def getfile(opath,loc,conn = reqs):
                                opath.replace('\\','/',-1)
                                opath.replace('//','/',-1)
                                loc.replace('\\','/',-1)
                                loc.replace('//','/',-1)
                                if loc[-1] != '/':
                                    loc += '/'
                                file = open(loc+opath[opath.rfind('/')+1:],'wb')
                                conn.send(bytes('giveme '+opath[6:],'utf-8'))
                                while True:
                                    b = conn.recv(2**32)
                                    try:
                                        if b.decode('utf-8') == 'EOF':
                                            break
                                    except:
                                        file.seek(0,2)
                                        file.write(b)
                                file.close()

                            addr = 'other '
                            self.browse()
                        else:
                            pass




    def browse(self):
        global addr
        if type(addr) == type(''):
            addr = addr.replace('//','/',-1)
        if addr != None:
            if addr == 'other ':
                print ('sendinng req')
                il = ogetitems('')
                print('hey')
                print('itemlist')
                self.TableWidget.set_table(il)
            elif addr[:6] == 'other ':
                #print('****')
                print(addr)
                self.lineEdit.setText(addr)
                il = ogetitems(addr[6:])
                print('itemlist',[i.name for i in il])
                self.TableWidget.set_table(il)
            else:
                addr = self.lineEdit.text()
                if os.path.isfile(addr):
                    os.startfile(addr)
                    self.lineEdit.setText(addr)
                    root = self.fileSystemModel.setRootPath(addr)
                    self.TreeView.setRootIndex(root)
                elif os.path.isdir(addr):
                    self.lineEdit.setText(addr)
                    root = self.fileSystemModel.setRootPath(addr)
                    self.TreeView.setRootIndex(root)
                    self.TableWidget.set_table(self.TableWidget.getItems(addr))
                elif addr=='':
                    items =[]
                    available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
                    for item in available_drives:
                        curr_item = Item(item, 0, '--', '--')
                        items.append(curr_item)
                    self.TableWidget.set_table(items)

                else:
                    self.raiseerror()
        else:
            self.TableWidget.set_table()
    def raiseerror(self):
        dialog = QtWidgets.QDialog()
        ex = Ui_Dialog()
        ex.setupUi(dialog)
        dialog.activateWindow()
        dialog.exec_()
        dialog.show()

    def up(self):
        global addr#
        if addr == '':
            self.pre = ''
            addr = None
            self.browse()
        elif addr == 'other ':
            self.pre = 'other '
            addr = None
            self.browse()
        if addr:
            if addr[-1] != '/':
                addr += '/'
            if addr.count('/')+addr.count('\\') <2:
                self.pre = addr
                if addr[:6] == 'other ':
                    addr = 'other '
                else:
                    addr = ''
                self.lineEdit.setText(str(addr))
                self.browse()
            else:
                self.pre = addr
                if addr[-1] == '/':
                    s = addr[:-1]
                else:
                    s = addr
                s = s.replace('\\', '/', -1)
                n = s.rfind('/')
                s = s[:n]+'/'
                addr = str(s)
                self.lineEdit.setText(str(s))
                self.browse()


    def back(self):
        global addr
        addr = self.pre
        self.lineEdit.setText(addr)
        self.browse()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "File Mnager"))
        self.label.setText(_translate("MainWindow", "Tree view"))
        self.pushButton_3.setText(_translate("MainWindow", "browse"))

    def clipboard(self, path, bul):
        self.TableWidget.clipboard = [path.replace('\\', '/', -1), bul]


import icons

if __name__ == "__main__":
    global addr
    addr = None
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec_())
