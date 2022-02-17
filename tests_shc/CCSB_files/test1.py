import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from pathlib import Path

class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi(r"C:\Users\kjaps\Downloads\testing1.ui",self)
        self.browse.clicked.connect(self.browsefiles)

    def browsefiles(self):
        filename=QFileDialog.getOpenFileName(self, 'Open file', r'C:\Users\kjaps\Downloads\testing1.ui', 'Images (*.dcm, *.jpg)')
        self.fileName.setText(filename[0])

        self.file_list = []
        [self.file_list.append(path) for path in filename]

        [print(f) for f in self.file_list]

app=QApplication(sys.argv)

mainwindow=MainWindow()

widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(400)
widget.setFixedHeight(300)
widget.show()

sys.exit(app.exec_())