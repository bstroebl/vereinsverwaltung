# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Ui_Suche.ui'
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

class Ui_Suche(object):
    def setupUi(self, Suche):
        Suche.setObjectName(_fromUtf8("Suche"))
        Suche.setWindowModality(QtCore.Qt.ApplicationModal)
        Suche.resize(400, 369)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Suche)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tblSuchKriterium = QtGui.QTableView(Suche)
        self.tblSuchKriterium.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblSuchKriterium.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblSuchKriterium.setObjectName(_fromUtf8("tblSuchKriterium"))
        self.horizontalLayout.addWidget(self.tblSuchKriterium)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btnUnd = QtGui.QPushButton(Suche)
        self.btnUnd.setObjectName(_fromUtf8("btnUnd"))
        self.verticalLayout.addWidget(self.btnUnd)
        self.pushButton = QtGui.QPushButton(Suche)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.txtSuche = QtGui.QPlainTextEdit(Suche)
        self.txtSuche.setObjectName(_fromUtf8("txtSuche"))
        self.verticalLayout_2.addWidget(self.txtSuche)
        self.buttonBox = QtGui.QDialogButtonBox(Suche)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Suche)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Suche.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Suche.reject)
        QtCore.QMetaObject.connectSlotsByName(Suche)

    def retranslateUi(self, Suche):
        Suche.setWindowTitle(_translate("Suche", "Suche", None))
        self.btnUnd.setText(_translate("Suche", "Und", None))
        self.pushButton.setText(_translate("Suche", "Oder", None))

