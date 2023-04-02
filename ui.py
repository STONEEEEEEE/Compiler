from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("File Manager")
        MainWindow.resize(1120, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setGeometry(QtCore.QRect(10, 80, 121, 41))

        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 190, 221, 471))
        self.listView.setObjectName("listView")
        path = r"E:\PycharmProjects"
        self.dirModel = QtWidgets.QFileSystemModel()
        self.dirModel.setRootPath(QtCore.QDir.rootPath())
        self.listView.setModel(self.dirModel)
        self.listView.setRootIndex(self.dirModel.index(path))


        self.fileModel = QtWidgets.QFileSystemModel()
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setModel(self.fileModel)
        self.treeView.setRootIndex(self.fileModel.index(path))
        self.treeView.setGeometry(QtCore.QRect(270, 90, 801, 571))
        self.treeView.setObjectName("treeView")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("File Manager", "File Manager"))
        self.button1.setText(_translate("MainWindow", "+ New File"))