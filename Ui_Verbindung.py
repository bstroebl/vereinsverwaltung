# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Ui_Verbindung.ui'
#
# Created by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Verbindung(object):
    def setupUi(self, Verbindung):
        Verbindung.setObjectName(_fromUtf8("Verbindung"))
        Verbindung.resize(368, 259)
        self.verticalLayout = QtGui.QVBoxLayout(Verbindung)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Verbindung)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.cbxType = QtGui.QComboBox(Verbindung)
        self.cbxType.setObjectName(_fromUtf8("cbxType"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cbxType)
        self.label_2 = QtGui.QLabel(Verbindung)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.host = QtGui.QLineEdit(Verbindung)
        self.host.setObjectName(_fromUtf8("host"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.host)
        self.label_3 = QtGui.QLabel(Verbindung)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.port = QtGui.QLineEdit(Verbindung)
        self.port.setObjectName(_fromUtf8("port"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.port)
        self.label_4 = QtGui.QLabel(Verbindung)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.database = QtGui.QLineEdit(Verbindung)
        self.database.setObjectName(_fromUtf8("database"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.database)
        self.label_5 = QtGui.QLabel(Verbindung)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.user = QtGui.QLineEdit(Verbindung)
        self.user.setObjectName(_fromUtf8("user"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.user)
        self.label_6 = QtGui.QLabel(Verbindung)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.password = QtGui.QLineEdit(Verbindung)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.password)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Verbindung)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Verbindung)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Verbindung.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Verbindung.reject)
        QtCore.QMetaObject.connectSlotsByName(Verbindung)

    def retranslateUi(self, Verbindung):
        Verbindung.setWindowTitle(_translate("Verbindung", "Verbindungseinstellungen", None))
        self.label.setText(_translate("Verbindung", "Verbindungstyp", None))
        self.label_2.setText(_translate("Verbindung", "Host", None))
        self.label_3.setText(_translate("Verbindung", "Port", None))
        self.label_4.setText(_translate("Verbindung", "Datenbank", None))
        self.label_5.setText(_translate("Verbindung", "User", None))
        self.label_6.setText(_translate("Verbindung", "Passwort", None))

