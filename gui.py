from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
        QRadioButton, QHBoxLayout, QVBoxLayout, QStyleFactory, QLineEdit,
        QTextEdit, QLabel, QPushButton, QTabWidget, QWidget, QButtonGroup,
        QDateEdit, QCheckBox, QShortcut, QTextBrowser)
from utils import save_entry
import codecs


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.createCategorySelectionGroupBox()
        self.createTextEditLayout()
        self.createButtonLayout()

        mainLayout = QGridLayout()
        mainLayout.addLayout(self.categorySelectionLayout, 0, 0)
        mainLayout.addLayout(self.textEditLayout, 1, 0)
        mainLayout.addLayout(self.buttonLayout, 2, 0)
        self.setLayout(mainLayout)

        QApplication.setStyle(QStyleFactory.create("cleanlooks"))
        self.setWindowTitle("FK-tiedotin")
        self.setWindowIcon(QtGui.QIcon('templates/fi.png'))



    def createCategorySelectionGroupBox(self):
        self.languageCheckBox = QCheckBox("Text in English", self)
        self.languageCheckBox.stateChanged.connect(self.languageCheckBoxClicked)

        self.toBothBulletinsCheckBox = QCheckBox("Add to both versions", self)

        categorySelectionGroupBox = QGroupBox("Category")
        self.categorySelectionButtonGroup = QButtonGroup()

        self.radioButton1 = QRadioButton("Killan tapahtumat")
        self.radioButton2 = QRadioButton("Muut tapahtumat")
        self.radioButton3 = QRadioButton("Yleistä")
        self.radioButton4 = QRadioButton("Opinnot")
        self.radioButton1.setChecked(True)

        self.categorySelectionButtonGroup.addButton(self.radioButton1)
        self.categorySelectionButtonGroup.addButton(self.radioButton2)
        self.categorySelectionButtonGroup.addButton(self.radioButton3)
        self.categorySelectionButtonGroup.addButton(self.radioButton4)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.radioButton1)
        buttonLayout.addWidget(self.radioButton2)
        buttonLayout.addWidget(self.radioButton3)
        buttonLayout.addWidget(self.radioButton4)
        categorySelectionGroupBox.setLayout(buttonLayout)

        self.dateEdit = QDateEdit()
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        self.dateEdit.setCalendarPopup(True)

        dateLabel = QLabel("Date")
        dateLabel.setBuddy(self.dateEdit)

        self.categorySelectionLayout = QVBoxLayout()
        self.categorySelectionLayout.addWidget(self.languageCheckBox)
        self.categorySelectionLayout.addWidget(self.toBothBulletinsCheckBox)
        self.categorySelectionLayout.addWidget(categorySelectionGroupBox)
        self.categorySelectionLayout.addWidget(dateLabel)
        self.categorySelectionLayout.addWidget(self.dateEdit)



    def languageCheckBoxClicked(self,state):
        if state == QtCore.Qt.Checked:
            self.radioButton1.setText("Guild's events")
            self.radioButton2.setText("Other events")
            self.radioButton3.setText("General")
            self.radioButton4.setText("Studies")
        else:
            self.radioButton1.setText("Killan tapahtumat")
            self.radioButton2.setText("Muut tapahtumat")
            self.radioButton3.setText("Yleistä")
            self.radioButton4.setText("Opinnot")




    #def hide(self):
    #    self.headerLineEdit.hide()
    #    self.textBrowser = QTextBrowser()
    #    self.textBrowser.setGeometry(QtCore.QRect(390, 10, 531, 681))
    #    self.textBrowser.setObjectName("textBrowser")
    #    self.textBrowser.show()


    def createTextEditLayout(self):
        self.textEditLayout = QVBoxLayout()

        self.headerLineEdit = QLineEdit()
        self.contentTextEdit = QTextEdit()

        headerLabel = QLabel("Header")
        headerLabel.setBuddy(self.headerLineEdit)

        contentLabel = QLabel("Content")
        contentLabel.setBuddy(self.contentTextEdit)

        self.textEditLayout.addWidget(headerLabel)
        self.textEditLayout.addWidget(self.headerLineEdit)
        self.textEditLayout.addWidget(contentLabel)
        self.textEditLayout.addWidget(self.contentTextEdit)



    def createButtonLayout(self):
        self.buttonLayout = QHBoxLayout()

        savePushButton = QPushButton("Save")
        savePushButton.clicked.connect(self.save)

        clearPushButton = QPushButton("Clear")
        clearPushButton.clicked.connect(self.clear)

        self.buttonLayout.addWidget(clearPushButton)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(savePushButton)


    def save(self):
        category = self.categorySelectionButtonGroup.checkedButton().text()
        date = [self.dateEdit.date().day(), self.dateEdit.date().month(), self.dateEdit.date().year()]
        header = self.headerLineEdit.text()
        content = self.contentTextEdit.toPlainText()

        save_entry({
            'category': category,
            'date': date,
            'header': header,
            'content': content
            }, self.languageCheckBox.isChecked())

        if self.toBothBulletinsCheckBox.isChecked():
            save_entry({
                'category': category,   # both languages fix here
                'date': date,
                'header': header,
                'content': content
                }, not self.languageCheckBox.isChecked())

        self.clear()


    def clear(self):
        self.headerLineEdit.clear()
        self.contentTextEdit.clear()
        self.languageCheckBox.setCheckState(0)
        self.toBothBulletinsCheckBox.setCheckState(0)
        self.dateEdit.setDateTime(QDateTime.currentDateTime())



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    tiedotin = MainWindow()
    tiedotin.show()
    sys.exit(app.exec_())
