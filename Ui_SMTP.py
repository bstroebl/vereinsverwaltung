# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Ui_SMTP.ui'
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

class Ui_SMTP(object):
    def setupUi(self, SMTP):
        SMTP.setObjectName(_fromUtf8("SMTP"))
        SMTP.resize(281, 284)
        self.gridLayout = QtGui.QGridLayout(SMTP)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(SMTP)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.host = QtGui.QLineEdit(SMTP)
        self.host.setObjectName(_fromUtf8("host"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.host)
        self.label_3 = QtGui.QLabel(SMTP)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.port = QtGui.QLineEdit(SMTP)
        self.port.setObjectName(_fromUtf8("port"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.port)
        self.label = QtGui.QLabel(SMTP)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.chkSSL = QtGui.QCheckBox(SMTP)
        self.chkSSL.setObjectName(_fromUtf8("chkSSL"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.chkSSL)
        self.label_5 = QtGui.QLabel(SMTP)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.user = QtGui.QLineEdit(SMTP)
        self.user.setObjectName(_fromUtf8("user"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.user)
        self.label_6 = QtGui.QLabel(SMTP)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.password = QtGui.QLineEdit(SMTP)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.password)
        self.label_7 = QtGui.QLabel(SMTP)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_7)
        self.senderName = QtGui.QLineEdit(SMTP)
        self.senderName.setObjectName(_fromUtf8("senderName"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.senderName)
        self.label_8 = QtGui.QLabel(SMTP)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_8)
        self.sender = QtGui.QLineEdit(SMTP)
        self.sender.setObjectName(_fromUtf8("sender"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.sender)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SMTP)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(SMTP)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SMTP.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SMTP.reject)
        QtCore.QMetaObject.connectSlotsByName(SMTP)

    def retranslateUi(self, SMTP):
        SMTP.setWindowTitle(_translate("SMTP", "SMTP-Server", None))
        self.label_2.setText(_translate("SMTP", "Server", None))
        self.host.setToolTip(_translate("SMTP", "Adresse der SMTP-Servers", None))
        self.label_3.setText(_translate("SMTP", "Port", None))
        self.port.setToolTip(_translate("SMTP", "optional: Port des SMTP-Servers", None))
        self.label.setText(_translate("SMTP", "Sicherheit", None))
        self.chkSSL.setToolTip(_translate("SMTP", "soll SSL benutzt werden", None))
        self.chkSSL.setText(_translate("SMTP", "SSL", None))
        self.label_5.setText(_translate("SMTP", "User", None))
        self.user.setToolTip(_translate("SMTP", "Username für die Anmeldung am SMTP-Server", None))
        self.label_6.setText(_translate("SMTP", "Passwort", None))
        self.password.setToolTip(_translate("SMTP", "Passwort für die Anmeldung am SMTP-Server", None))
        self.label_7.setText(_translate("SMTP", "Name des Absenders", None))
        self.senderName.setToolTip(_translate("SMTP", "optional", None))
        self.label_8.setText(_translate("SMTP", "Absenderadresse", None))
        self.sender.setToolTip(_translate("SMTP", "geben Sie die Email-Adresse ein, die als Absender auf Ihren Mails erscheint", None))

