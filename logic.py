from PyQt5.QtWidgets import *
from ui import Ui_MainWindow
import sys

class Logic(Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        # Set up the user interface
        self.setupUi(self)

        # "New Project" button function call
        self.button1.clicked.connect(self.make_document)

        # When folder in listView is clicked, the items stored in it are
        # displayed in the treeview.
        self.listView.clicked.connect(self.on_click)

    # Program Functions
    def on_click(self, index):
        """When a directory is selected in the list view, show all of its files
        in the tree view."""
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.treeView.setRootIndex(self.fileModel.setRootPath(path))

    def make_document(self):
        print("Making document")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
