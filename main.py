from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import subprocess
from pathlib import Path
import threading

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 250)
        MainWindow.setMinimumSize(QtCore.QSize(300, 250))
        MainWindow.setMaximumSize(QtCore.QSize(300, 250))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.folderButton = QtWidgets.QPushButton(self.centralwidget)
        self.folderButton.setEnabled(False)
        self.folderButton.setGeometry(QtCore.QRect(60, 30, 93, 28))
        self.folderButton.setObjectName("folderButton")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 55, 16))
        self.label.setObjectName("label")
        self.label.setGeometry(QtCore.QRect(10, 10, 271, 16))

        self.fileButton = QtWidgets.QPushButton(self.centralwidget)
        self.fileButton.setGeometry(QtCore.QRect(160, 30, 93, 28))
        self.fileButton.setObjectName("fileButton")
        self.fileButton.clicked.connect(self.setFile)

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(110, 90, 93, 28))
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.setDirectory)
        self.saveButton.setEnabled(False)

        self.convertButton = QtWidgets.QPushButton(self.centralwidget)
        self.convertButton.setGeometry(QtCore.QRect(110, 130, 93, 28))
        self.convertButton.setObjectName("convertButton")
        self.convertButton.clicked.connect(self.convertIt)
        self.convertButton.setEnabled(False)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 55, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QtCore.QRect(10, 70, 271, 16))

        self.infoButton = QtWidgets.QPushButton(self.centralwidget)
        self.infoButton.setGeometry(QtCore.QRect(110, 170, 93, 28))
        self.infoButton.setObjectName("infoButton")
        self.infoButton.clicked.connect(self.showInfo)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage('Hi!')

        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def showInfo(self):
        msg = QMessageBox()
        msg.setWindowTitle("Info...")
        msg.setText("Created by: Adam Fatyga\n"
                    "Email: adamfatyga@protonmail.com\n"
                    "Find me on LinkedIn!")
        msg.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "mkv to mp4"))
        self.folderButton.setText(_translate("MainWindow", "Select folder"))
        self.label.setText(_translate("MainWindow", "None"))
        self.fileButton.setText(_translate("MainWindow", "Select file"))
        self.saveButton.setText(_translate("MainWindow", "Save to..."))
        self.convertButton.setText(_translate("MainWindow", "Convert"))
        self.label_2.setText(_translate("MainWindow", "None"))
        self.infoButton.setText(_translate("MainWindow", "Info"))

    def setFile(self):
        global fileName
        fileName = QFileDialog.getOpenFileName(None, "1", "", "MKV files (*.mkv);;All files (*)")
        self.label.setText(fileName[0])
        self.saveButton.setEnabled(True)

    def setDirectory(self):
        global saveDirectory
        saveDirectory = QFileDialog.getExistingDirectory(None, "Select folder", "")
        if saveDirectory[-1] != "/":
            saveDirectory += "/"
        self.label_2.setText(saveDirectory)
        self.convertButton.setEnabled(True)

    def converting(self):
        global saveDirectory, fileName
        try:
            print(saveDirectory, 'jest zmienna')
        except:
            print("Brak zmiennej")
        onlyFileName = Path(fileName[0]).stem
        saveDirectory = ""
        saveDirectory = f"{saveDirectory}{onlyFileName}.mp4"
        print(saveDirectory, 'save directory')
        subprocess.run(['ffmpeg', '-i', str(fileName[0]), '-codec', 'copy', saveDirectory], check=True)
        self.statusbar.showMessage('Done!')
        self.convertButton.setEnabled(True)

        # Convert it!
    def convertIt(self):
        self.statusbar.showMessage('Im working...')
        self.convertButton.setEnabled(False)
        try:
            threading.Thread(target=self.converting).start()
        except Exception as e:
            self.statusbar.showMessage('Error! Write to: fornakter@gmail.com')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
