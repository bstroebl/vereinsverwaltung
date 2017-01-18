# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Ui_MitgliedNatuerlich.ui'
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

class Ui_MitgliedNatuerlich(object):
    def setupUi(self, MitgliedNatuerlich):
        MitgliedNatuerlich.setObjectName(_fromUtf8("MitgliedNatuerlich"))
        MitgliedNatuerlich.resize(293, 457)
        self.verticalLayout = QtGui.QVBoxLayout(MitgliedNatuerlich)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(MitgliedNatuerlich)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.cbxAnrede = QtGui.QComboBox(MitgliedNatuerlich)
        self.cbxAnrede.setObjectName(_fromUtf8("cbxAnrede"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cbxAnrede)
        self.label_16 = QtGui.QLabel(MitgliedNatuerlich)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_16)
        self.txlTitel = QtGui.QLineEdit(MitgliedNatuerlich)
        self.txlTitel.setObjectName(_fromUtf8("txlTitel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.txlTitel)
        self.label_3 = QtGui.QLabel(MitgliedNatuerlich)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.txlVorname = QtGui.QLineEdit(MitgliedNatuerlich)
        self.txlVorname.setObjectName(_fromUtf8("txlVorname"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.txlVorname)
        self.label_4 = QtGui.QLabel(MitgliedNatuerlich)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.txlName = QtGui.QLineEdit(MitgliedNatuerlich)
        self.txlName.setObjectName(_fromUtf8("txlName"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.txlName)
        self.label_5 = QtGui.QLabel(MitgliedNatuerlich)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.txlNamenszusatz = QtGui.QLineEdit(MitgliedNatuerlich)
        self.txlNamenszusatz.setObjectName(_fromUtf8("txlNamenszusatz"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.txlNamenszusatz)
        self.label_6 = QtGui.QLabel(MitgliedNatuerlich)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.dateGeburtsdatum = QtGui.QDateEdit(MitgliedNatuerlich)
        self.dateGeburtsdatum.setEnabled(True)
        self.dateGeburtsdatum.setCalendarPopup(True)
        self.dateGeburtsdatum.setObjectName(_fromUtf8("dateGeburtsdatum"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.dateGeburtsdatum)
        self.label_2 = QtGui.QLabel(MitgliedNatuerlich)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_2)
        self.txlBeruf = QtGui.QLineEdit(MitgliedNatuerlich)
        self.txlBeruf.setObjectName(_fromUtf8("txlBeruf"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.txlBeruf)
        self.verticalLayout.addLayout(self.formLayout)
        self.label_8 = QtGui.QLabel(MitgliedNatuerlich)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout.addWidget(self.label_8)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.txlHauptmitglied = QtGui.QLineEdit(MitgliedNatuerlich)
        self.txlHauptmitglied.setReadOnly(True)
        self.txlHauptmitglied.setObjectName(_fromUtf8("txlHauptmitglied"))
        self.horizontalLayout_2.addWidget(self.txlHauptmitglied)
        self.btnShowHauptmitglied = QtGui.QPushButton(MitgliedNatuerlich)
        self.btnShowHauptmitglied.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/view_detailed.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnShowHauptmitglied.setIcon(icon)
        self.btnShowHauptmitglied.setFlat(True)
        self.btnShowHauptmitglied.setObjectName(_fromUtf8("btnShowHauptmitglied"))
        self.horizontalLayout_2.addWidget(self.btnShowHauptmitglied)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_19 = QtGui.QLabel(MitgliedNatuerlich)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.verticalLayout.addWidget(self.label_19)
        self.txtHinweise = QtGui.QPlainTextEdit(MitgliedNatuerlich)
        self.txtHinweise.setObjectName(_fromUtf8("txtHinweise"))
        self.verticalLayout.addWidget(self.txtHinweise)
        self.label.setBuddy(self.cbxAnrede)
        self.label_16.setBuddy(self.txlTitel)
        self.label_3.setBuddy(self.txlVorname)
        self.label_4.setBuddy(self.txlName)
        self.label_5.setBuddy(self.txlNamenszusatz)
        self.label_6.setBuddy(self.dateGeburtsdatum)

        self.retranslateUi(MitgliedNatuerlich)
        QtCore.QMetaObject.connectSlotsByName(MitgliedNatuerlich)
        MitgliedNatuerlich.setTabOrder(self.cbxAnrede, self.txlTitel)
        MitgliedNatuerlich.setTabOrder(self.txlTitel, self.txlVorname)
        MitgliedNatuerlich.setTabOrder(self.txlVorname, self.txlName)
        MitgliedNatuerlich.setTabOrder(self.txlName, self.txlNamenszusatz)
        MitgliedNatuerlich.setTabOrder(self.txlNamenszusatz, self.dateGeburtsdatum)
        MitgliedNatuerlich.setTabOrder(self.dateGeburtsdatum, self.txlBeruf)
        MitgliedNatuerlich.setTabOrder(self.txlBeruf, self.txlHauptmitglied)
        MitgliedNatuerlich.setTabOrder(self.txlHauptmitglied, self.btnShowHauptmitglied)

    def retranslateUi(self, MitgliedNatuerlich):
        MitgliedNatuerlich.setWindowTitle(_translate("MitgliedNatuerlich", "Form", None))
        self.label.setText(_translate("MitgliedNatuerlich", "&Anrede", None))
        self.label_16.setText(_translate("MitgliedNatuerlich", "&Titel", None))
        self.label_3.setText(_translate("MitgliedNatuerlich", "&Vorname", None))
        self.label_4.setText(_translate("MitgliedNatuerlich", "&Nachname", None))
        self.label_5.setText(_translate("MitgliedNatuerlich", "Namens&zusatz", None))
        self.label_6.setText(_translate("MitgliedNatuerlich", "&Geburtsdatum", None))
        self.dateGeburtsdatum.setDisplayFormat(_translate("MitgliedNatuerlich", "dd.MM.yyyy", None))
        self.label_2.setText(_translate("MitgliedNatuerlich", "Beruf", None))
        self.label_8.setText(_translate("MitgliedNatuerlich", "zugehöriges Hauptmitglied", None))
        self.btnShowHauptmitglied.setToolTip(_translate("MitgliedNatuerlich", "Hauptmitglied anzeigen", None))
        self.label_19.setText(_translate("MitgliedNatuerlich", "Hinweise", None))

import resources_rc
