# coding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from eventsDetectGUI import Ui_MainWindow
from Function import detectMainFast
from multiprocessing import freeze_support
import frozen

if __name__ == "__main__":
    freeze_support()
    class MyMainWindow(QMainWindow, Ui_MainWindow):
        def __init__(self, parent=None):
            super(MyMainWindow, self).__init__(parent)
            self.setupUi(self)
            self.lineEdit_pattern.setText("down")
            self.lineEdit_startCoeff.setText("5")
            self.lineEdit_endCoeff.setText("0")
            self.lineEdit_filterCoeff.setText("0.99")
            self.lineEdit_minDuration.setText("0")
            self.lineEdit_maxDuration.setText("10")
            self.pushButton_selectFile.clicked.connect(self.getFile)
            self.pushButton_start.clicked.connect(self.detect)

        def getFile(self):
            fileNames, _ = QFileDialog.getOpenFileNames(self, 'Select File', 'c:/', "Axon Binary File(*.abf)")
            fileList = ';'.join(fileNames)
            self.textBrowser_fileName.setPlainText(fileList)

        def detect(self):
            pattern = self.lineEdit_pattern.text()
            startCoeff = int(self.lineEdit_startCoeff.text())
            endCoeff = int(self.lineEdit_endCoeff.text())
            filterCoeff = float(self.lineEdit_filterCoeff.text())
            minDuration = float(self.lineEdit_minDuration.text())
            maxDuration = float(self.lineEdit_maxDuration.text())
            fileNames = self.textBrowser_fileName.toPlainText()
            fileList = fileNames.split(";")
            if fileList == ['']:
                self.showNoFileErrorMessageBox()
            else:
                detectMainFast(fileList, pattern, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration)

        def showNoFileErrorMessageBox(self):
            QMessageBox.critical(self, "NoFileError", "Please select files before detecting",)

    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())

