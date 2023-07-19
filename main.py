import datetime
import pathlib

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

        # Folder button
        self.selectFolderButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectFolderButton.setEnabled(True)
        self.selectFolderButton.setGeometry(QtCore.QRect(60, 30, 93, 28))
        self.selectFolderButton.setObjectName("folderButton")
        self.selectFolderButton.clicked.connect(self.folderButtonClick)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 55, 16))
        self.label.setObjectName("label")
        self.label.setGeometry(QtCore.QRect(10, 10, 271, 16))

        self.selectFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectFileButton.setGeometry(QtCore.QRect(160, 30, 93, 28))
        self.selectFileButton.setObjectName("fileButton")
        self.selectFileButton.clicked.connect(self.setFile)

        self.saveToFolderButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveToFolderButton.setGeometry(QtCore.QRect(110, 90, 93, 28))
        self.saveToFolderButton.setObjectName("saveButton")
        self.saveToFolderButton.clicked.connect(self.setDirectory)
        self.saveToFolderButton.setEnabled(False)

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

    def folderButtonClick(self):
        selectFolderToOpen = QFileDialog.getExistingDirectory(None, "Select folder", "")
        self.label.setText(selectFolderToOpen)
        print(selectFolderToOpen)
        self.saveToFolderButton.setEnabled(True)

        # Show window title with info
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
        self.selectFolderButton.setText(_translate("MainWindow", "Select folder"))
        self.label.setText(_translate("MainWindow", "None"))
        self.selectFileButton.setText(_translate("MainWindow", "Select file"))
        self.saveToFolderButton.setText(_translate("MainWindow", "Save to..."))
        self.convertButton.setText(_translate("MainWindow", "Convert"))
        self.label_2.setText(_translate("MainWindow", "None"))
        self.infoButton.setText(_translate("MainWindow", "Info"))

        # Select file, dialog window
    def setFile(self):
        global wholeFileName
        wholeFileName = QFileDialog.getOpenFileName(None, "1", "", "MKV files (*.mkv);;AVI files (*.avi);;All files (*)")
        self.label.setText(wholeFileName[0])
        self.saveToFolderButton.setEnabled(True)

        # Select directory to save, dialog window
    def setDirectory(self):
        global saveDirectory
        saveDirectory = QFileDialog.getExistingDirectory(None, "Select folder", "")
        if saveDirectory[-1] != "/":
            saveDirectory += "/"
        self.label_2.setText(saveDirectory)
        self.convertButton.setEnabled(True)

        # Converting
    def converting(self):
        global saveDirectory, wholeFileName
        fileExtension = wholeFileName[0][-4:]
        onlyFileName = Path(wholeFileName[0]).stem
        saveToDirectory = f"{saveDirectory}{onlyFileName}.mp4"
        try:
            if fileExtension == ".mkv":
                subprocess.run(['ffmpeg', '-i', str(wholeFileName[0]), '-codec', 'copy', '-y', saveToDirectory], check=True)
            else:
                subprocess.run(['ffmpeg', '-i', str(wholeFileName[0]), '-vcodec', 'copy', '-acodec', 'copy', saveToDirectory], check=True)
            self.statusbar.showMessage('Done!')
        except Exception as e:
            print(e)
            self.statusbar.showMessage('Error! Send me log!')
            errorFile = open("ErrorLog.txt", "a", encoding="utf8")
            errorFile.write(f'{str(datetime.datetime.now())}\n')
            errorFile.write(f'{str(e)}\nfileExtension: {fileExtension}\nonlyFileName: {onlyFileName}\n')
            errorFile.close()

        self.convertButton.setEnabled(True)
        self.selectFileButton.setEnabled(True)
        self.saveToFolderButton.setEnabled(True)

        # Convert button
    def convertIt(self):
        self.statusbar.showMessage('Im working...')
        self.convertButton.setEnabled(False)
        self.selectFileButton.setEnabled(False)
        self.saveToFolderButton.setEnabled(False)
        try:
            threading.Thread(target=self.converting).start()
        except Exception as e:
            print(e)
            self.statusbar.showMessage('Error! Send me log!')
            errorFile = open("ErrorLog.txt", "a", encoding="utf8")
            errorFile.write(f'{str(datetime.datetime.now())}\n')
            errorFile.write(f'{str(e)}\n')
            errorFile.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
