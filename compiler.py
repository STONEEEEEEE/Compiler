import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QIODevice, QTextStream
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QTreeWidgetItem
from GUI import Ui_MainWindow
from autoLexer import AutoLexer
from lexer import Lexer
from textWithLineNum import QTextEditWithLineNum


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # 窗口初始化
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 向textEdits列表添加初始化的空白选项卡中的文本框
        self.textEdits.append(self.textEdit_0)

        # 信号槽
        self.actionOpenFile.triggered.connect(self.openFile)
        self.actionNewFile.triggered.connect(self.newFile)
        self.actionSaveFile.triggered.connect(self.saveFile)
        self.tabWidget.tabCloseRequested.connect(self.tabClose)
        self.actionCompile.triggered.connect(self.lexAnalysis)

    # 业务逻辑代码
    filePath = []  # 保存每一张选项卡内的文件路径
    textEdits = []  # 记录每一张选项卡的textEdit对象

    # 添加新选项卡
    def addTab(self, fileName):
        newTab = QtWidgets.QWidget()
        newTab.setObjectName("tab_" + str(self.tabWidget.currentIndex()))
        newVLayout = QtWidgets.QVBoxLayout(newTab)
        newVLayout.setObjectName("verticalLayout_" + str(self.tabWidget.currentIndex() + 3))
        newTextEdit = QTextEditWithLineNum(newTab)
        # 设置不自动换行
        self.textEdits.append(newTextEdit)
        newTextEdit.setObjectName("textEdit" + str(self.tabWidget.currentIndex() + 1))
        newVLayout.addWidget(newTextEdit)
        self.tabWidget.addTab(newTab, fileName)

    # 选项卡删除
    def tabClose(self):
        self.tabWidget.tabBar().removeTab(self.tabWidget.currentIndex())

    # 关闭窗口时弹出确认消息
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', '确认退出？', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def openFile(self):
        dir = QFileDialog()  # 创建文件对话框
        if not dir.exec_():
            return
        file = QFile(dir.selectedFiles()[0])
        file.open(QIODevice.ReadOnly)
        read = QTextStream(file)
        read.setCodec("utf-8")
        filename = os.path.basename(dir.selectedFiles()[0])

        # 若打开文件时当前选项卡是空白选项卡，则将文件内容读入到空白选项卡中，否则创建新选项卡并读入文件
        if self.tabWidget.tabText(self.tabWidget.currentIndex()) != "空白选项卡":
            # 保存原文件
            self.saveFile()
            self.addTab(filename)
            # 切换到新选项卡
            self.tabWidget.setCurrentIndex(self.tabWidget.currentIndex() + 1)
        else:
            # 修改当前选项卡的标题为当前文件名
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), filename)
        # 直接在空白选项卡的文本框内读入文件内容
        nowTextEdit = self.textEdits[self.tabWidget.currentIndex()]
        nowTextEdit.clear()
        while not read.atEnd():
            nowTextEdit.append(read.readLine())

        file.close()
        # 记录文件路径
        self.filePath.append(os.path.dirname(__file__) + "\\" + filename)
        # 状态栏提示打开文件
        self.statusBar.showMessage("已打开文件" + self.filePath[self.tabWidget.currentIndex()], 5000)

    def newFile(self):
        # QInputDialog类是QtWidgets的子类
        # getText是静态方法，缺少一些设置参数，这时就要创建QInputDialog对象来设置
        filename, ok = QInputDialog.getText(mainWindow, "新建文件", "请输入新建文件名:", QtWidgets.QLineEdit.Normal)
        if not ok:
            return

        file = open(os.path.dirname(__file__) + "\\" + filename, "w")
        file.close()

        # 与打开文件判断一致
        if self.tabWidget.tabText(self.tabWidget.currentIndex()) != "空白选项卡":
            # 保存原文件
            self.saveFile()
            self.addTab(filename)
            # 切换到新选项卡
            self.tabWidget.setCurrentIndex(self.tabWidget.currentIndex() + 1)
        else:
            # 修改当前选项卡的标题为当前文件名
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), filename)

        # 记录文件路径
        self.filePath.append(os.path.dirname(__file__) + "\\" + filename)
        # 状态栏提示打开文件
        self.statusBar.showMessage("已新建文件" + self.filePath[self.tabWidget.currentIndex()], 5000)

    def saveFile(self):
        if self.filePath[self.tabWidget.currentIndex()] is not None:
            nowTextEdit = self.textEdits[self.tabWidget.currentIndex()]
            with open(file=self.filePath[self.tabWidget.currentIndex()], mode="w+", encoding="utf-8") as file:
                file.write(nowTextEdit.toPlainText())

            # 状态栏提示打开文件
            self.statusBar.showMessage("文件已保存到" + self.filePath[self.tabWidget.currentIndex()], 5000)

    def lexAnalysis(self):
        # 词法分析之前先保存
        self.saveFile()
        # 然后将当前选项卡的标题即文件名传给lexer
        filename = self.tabWidget.tabText(self.tabWidget.currentIndex())
        # 词法分析的结果是一个单词表
        # 单词表用列表存储，[单词, 所在行, 种别码]
        lexer = Lexer()
        lexer.start(filename)
        words = lexer.getWords()
        # 将单词表放入treewidget树状表
        for word in words:
            # 错误记入下面的文本框（）
            if word[2] == '0':
                item = QtWidgets.QListWidgetItem(self.listWidget)
                item.setText("error[" + word[1] + "]: " + word[0])
                continue
            item = QTreeWidgetItem(self.treeWidget)
            item.setText(0, word[0])
            item.setText(1, word[1])
            item.setText(2, word[2])
            self.treeWidget.addTopLevelItem(item)

    def autoLexAnalysis(self):
        self.saveFile()
        filename = self.tabWidget.tabText(self.tabWidget.currentIndex())

        # 词法分析的结果是一个单词表
        # 单词表用列表存储，[单词, 所在行, 种别码]
        autoLexer = AutoLexer()
        autoLexer.build()
        autoLexer.start(filename)
        # words = lexer.getWords()
        # # 将单词表放入treewidget树状表
        # for word in words:
        #     # 错误记入下面的文本框（）
        #     if word[2] == '0':
        #         item = QtWidgets.QListWidgetItem(self.listWidget)
        #         item.setText("error[" + word[1] + "]: " + word[0])
        #         continue
        #     item = QTreeWidgetItem(self.treeWidget)
        #     item.setText(0, word[0])
        #     item.setText(1, word[1])
        #     item.setText(2, word[2])
        #     self.treeWidget.addTopLevelItem(item)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()  # 创建窗体对象
    mainWindow.show()  # 显示窗体
    sys.exit(app.exec_())  # 程序关闭时退出进程