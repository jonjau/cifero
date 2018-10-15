# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(345, 141)
        self.gridLayout = QtWidgets.QGridLayout(SettingsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.SyllSepLabel = QtWidgets.QLabel(SettingsDialog)
        self.SyllSepLabel.setObjectName("SyllSepLabel")
        self.gridLayout.addWidget(self.SyllSepLabel, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 1, 1, 1)
        self.SentSepLabel = QtWidgets.QLabel(SettingsDialog)
        self.SentSepLabel.setObjectName("SentSepLabel")
        self.gridLayout.addWidget(self.SentSepLabel, 3, 0, 1, 1)
        self.SyllSepLineEdit = QtWidgets.QLineEdit(SettingsDialog)
        self.SyllSepLineEdit.setObjectName("SyllSepLineEdit")
        self.gridLayout.addWidget(self.SyllSepLineEdit, 2, 1, 1, 1)
        self.SentSepLineEdit = QtWidgets.QLineEdit(SettingsDialog)
        self.SentSepLineEdit.setObjectName("SentSepLineEdit")
        self.gridLayout.addWidget(self.SentSepLineEdit, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(SettingsDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.ResetButton = QtWidgets.QPushButton(SettingsDialog)
        self.ResetButton.setObjectName("ResetButton")
        self.gridLayout.addWidget(self.ResetButton, 5, 0, 1, 1)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings"))
        self.SyllSepLabel.setText(_translate("SettingsDialog", "Syllable Separator"))
        self.SentSepLabel.setText(_translate("SettingsDialog", "Word Separator"))
        self.label.setText(_translate("SettingsDialog", "* Make sure separators are unique"))
        self.ResetButton.setText(_translate("SettingsDialog", "Reset to Defaults"))

