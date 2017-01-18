# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Ui_MitgliedJuristisch.ui'
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

class Ui_MitgliedJuristisch(object):
    def setupUi(self, MitgliedJuristisch):
        MitgliedJuristisch.setObjectName(_fromUtf8("MitgliedJuristisch"))
        MitgliedJuristisch.resize(303, 244)
        self.verticalLayout = QtGui.QVBoxLayout(MitgliedJuristisch)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_4 = QtGui.QLabel(MitgliedJuristisch)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.txlName = QtGui.QLineEdit(MitgliedJuristisch)
        self.txlName.setObjectName(_fromUtf8("txlName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.txlName)
        self.label_14 = QtGui.QLabel(MitgliedJuristisch)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_14)
        self.txlAnsprechpartner = QtGui.QLineEdit(MitgliedJuristisch)
        self.txlAnsprechpartner.setObjectName(_fromUtf8("txlAnsprechpartner"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.txlAnsprechpartner)
        self.verticalLayout.addLayout(self.formLayout)
        self.label_19 = QtGui.QLabel(MitgliedJuristisch)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.verticalLayout.addWidget(self.label_19)
        self.txtHinweise = QtGui.QPlainTextEdit(MitgliedJuristisch)
        self.txtHinweise.setObjectName(_fromUtf8("txtHinweise"))
        self.verticalLayout.addWidget(self.txtHinweise)
        self.label_4.setBuddy(self.txlName)

        self.retranslateUi(MitgliedJuristisch)
        QtCore.QMetaObject.connectSlotsByName(MitgliedJuristisch)

    def retranslateUi(self, MitgliedJuristisch):
        MitgliedJuristisch.setWindowTitle(_translate("MitgliedJuristisch", "Form", None))
        self.label_4.setText(_translate("MitgliedJuristisch", "Mitglieds&name", None))
        self.label_14.setText(_translate("MitgliedJuristisch", "Ansprechpartner", None))
        self.label_19.setText(_translate("MitgliedJuristisch", "Hinweise", None))

