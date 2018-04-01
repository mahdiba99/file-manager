from PyQt5 import QtCore, QtGui, QtWidgets
import os,time,shutil
from dialog import Ui_Dialog
from Item import Item
from transfer import copy as fcopy ,cut as fcut
global addr

class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)
        self.clipboard = "Nothing yet"
        global addr
    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        CopyAction = menu.addAction("Copy")
        CutAction = menu.addAction("Cut")
        delAction= menu.addAction("Delete")
        newAction= menu.addAction("NewFolder")
        pasteAction = menu.addAction("Paste")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == delAction :
            remove_path = addr+'/'+str(self.item(self.currentRow(),self.currentColumn()).text())
            print(remove_path)
            delete(remove_path,None,self)
        if action == CopyAction:
            self.clipboard = [addr.replace('\\','/',-1)+'/'+str(self.item(self.currentRow(),self.currentColumn()).text()),False]
        if action == CutAction:
            self.clipboard = [addr.replace('\\','/',-1)+'/'+str(self.item(self.currentRow(),self.currentColumn()).text()),True]
        if action == newAction:
            newfolder(addr,None,self)
        if action == pasteAction:
            if self.clipboard == 'Nothing yet':
                print('no')
                pass
            else:
                if self.clipboard[1] == True:
                    print(self.clipboard[0],'------>>>>>',addr)
                    copy(self.clipboard[0],addr)
                    self.clipboard = 'Nothing yet'
                    delete(self.clipboard[0])
                else:
                    print(self.clipboard[0], '------>>>>>', addr)
                    copy(self.clipboard[0],addr)

def copy(source,destination):
    if os.path.isdir(source):
        shutil.copytree(source,destination)
    else:
        shutil.copyfile(source,destination)
def delete(address,ui = None,table = None):
    address = address.replace('\\','/',-1)
    if os.path.isdir(address):
        shutil.rmtree(address)
    else:
        os.remove(address)
    try:
        ui.set_table()
    except:
        table.removeRow(table.currentRow())
def newfolder(address,ui = None,table = None):
    try:
        os.makedirs(address+"\\"+"NewFolder")
    except:
        pass
    try:
        ui.set_table()
    except:
        pass



class Ui_MainWindow():
    def __init__(self):
        MainWindow = QtWidgets.QMainWindow()
        self.setupUi(MainWindow)
        MainWindow.show()
        self.fileIcon = QtGui.QIcon(QtGui.QPixmap("icons/file.png"))
        self.folderIcon = QtGui.QIcon(QtGui.QPixmap("icons/folder.png"))
        self.set_table()
        self.itemlocation = addr
        sys.exit(app.exec_())

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(1103, 864)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/مدارک/picture-24048-1508053366.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
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
        root = self.fileSystemModel.setRootPath("/")
        self.TreeView.setModel(self.fileSystemModel)
        self.TreeView.setRootIndex(root)

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
        self.pushButton_3.clicked.connect(self.browes)
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
        self.deletebutton.setGeometry(QtCore.QRect(300, 590, 93, 28))
        self.deletebutton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.deletebutton.setIcon(icon3)
        self.deletebutton.setIconSize(QtCore.QSize(30, 30))
        self.deletebutton.setFlat(True)
        self.deletebutton.setObjectName("deletebutton")
        self.deletebutton.clicked.connect(lambda:delete(self.itemlocation,self))
        self.newbutton = QtWidgets.QPushButton(self.centralwidget)
        self.newbutton.setGeometry(QtCore.QRect(410, 590, 93, 28))
        self.newbutton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/icons/newfolder.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.newbutton.setIcon(icon4)
        self.newbutton.setIconSize(QtCore.QSize(30, 30))
        self.newbutton.setFlat(True)
        self.newbutton.setObjectName("newbutton")
        self.newbutton.clicked.connect(lambda: newfolder(addr, self))
        self.copybutton = QtWidgets.QPushButton(self.centralwidget)
        self.copybutton.setGeometry(QtCore.QRect(520, 590, 93, 28))
        self.copybutton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/newPrefix/icons/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.copybutton.setIcon(icon5)
        self.copybutton.setIconSize(QtCore.QSize(30, 30))
        self.copybutton.setFlat(True)
        self.copybutton.setObjectName("copybutton")
        self.cutbutton = QtWidgets.QPushButton(self.centralwidget)
        self.cutbutton.setGeometry(QtCore.QRect(620, 590, 93, 28))
        self.cutbutton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/newPrefix/icons/Cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cutbutton.setIcon(icon6)
        self.cutbutton.setIconSize(QtCore.QSize(30, 30))
        self.cutbutton.setFlat(True)
        self.cutbutton.setObjectName("cutbutton")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def itemclicked(self,item):
        if item.column() == 0:
            self.itemlocation = addr+'\\'+str(item.data())

    def doubleClicked(self,item):
        global addr
        if item.column() == 0:
                if os.path.isdir(addr + "\\" + str(item.data())):
                    addr += "\\" + str(item.data())
                    self.lineEdit.setText(addr)
                    self.browes()
                else:
                    preaddr = addr
                    addr += "/" + str(item.data())
                    self.lineEdit.setText(addr)
                    self.browes()

                    addr = preaddr
                    self.lineEdit.setText(addr)




    def browes(self):
        global addr
        addr = self.lineEdit.text()
        if os.path.isfile(addr):
            os.startfile(addr)
            self.lineEdit.setText(addr)
            root = self.fileSystemModel.setRootPath(addr)
            self.TreeView.setRootIndex(root)
        elif os.path.isdir(addr):
            self.lineEdit.setText(addr)
            root = self.fileSystemModel.setRootPath(addr)
            self.set_table()
            self.TreeView.setRootIndex(root)
        else:
            self.raiseerror()

    def raiseerror(self):
        dialog = QtWidgets.QDialog()
        ex = Ui_Dialog()
        ex.setupUi(dialog)
        dialog.show()
        dialog.exec_()
    def up(self):
        global addr
        self.pre = os.getcwd()
        if os.getcwd()[-1] == '/':
            s = os.getcwd[:-1]
        else:
            s = os.getcwd()
        n = s.rfind('\\')
        s=s[:n]+'\\'
        os.chdir(s)#
        addr = str(s)
        self.lineEdit.setText(str(s))
        self.browes()
    def back(self):
        global addr
        os.chdir(self.pre)
        addr = str(os.getcwd())
        self.lineEdit.setText(addr)
        self.browes()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "File Mnager"))
        self.label.setText(_translate("MainWindow", "Tree view"))
        self.pushButton_3.setText(_translate("MainWindow", "browes"))

    def getItems(self,path):
        os.chdir(path)
        itemlist = os.listdir()
        items = []
        for item in  itemlist:
            tmp_item = Item(item,os.path.getsize(path + '/' + item) , time.ctime(os.path.getmtime(path + '/' + item)),path )
            items.append(tmp_item)
        return items
    def set_table(self):
        items = self.getItems(addr)
        for i in range(len(items)):
            self.TableWidget.setRowCount(len(items))
            self.TableWidget.setColumnCount(3)
            self.TableWidget.setHorizontalHeaderLabels(("Name", "Date Modified", "Size"))
            self.TableWidget.autoFillBackground()
            icon3 = self.fileIcon
            if os.path.isdir(items[i].path+"/"+items[i].name):
                icon3 = self.folderIcon
            self.TableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(icon3,items[i].name))
            self.TableWidget.setItem(i,1 , QtWidgets.QTableWidgetItem(items[i].date))
            if icon3 == self.folderIcon:
                self.TableWidget.setItem(i,2,QtWidgets.QTableWidgetItem("--"))
            else:
                if items[i].size // 1000000000 != 0:
                    size = str(round(items[i].size/1000000000,2)) + " GB"
                elif items[i].size // 1000000 != 0:
                    size = str(round(items[i].size/1000000,2)) + " MB"
                elif items[i].size // 1000 != 0:
                    size = str(round(items[i].size /1000,2)) + " KB"
                else :
                    size = str(items[i].size) + " B"
                self.TableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(size))
        self.TableWidget.resizeColumnsToContents()





import icons

if __name__ == "__main__":
    global addr
    addr = os.getcwd()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec_())
