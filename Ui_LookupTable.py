# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Ui_LookupTable.ui'
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

class Ui_LookupTable(object):
    def setupUi(self, LookupTable):
        LookupTable.setObjectName(_fromUtf8("LookupTable"))
        LookupTable.setWindowModality(QtCore.Qt.ApplicationModal)
        LookupTable.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(LookupTable)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tbl = QtGui.QTableView(LookupTable)
        self.tbl.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tbl.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.tbl.setSortingEnabled(True)
        self.tbl.setObjectName(_fromUtf8("tbl"))
        self.tbl.verticalHeader().setSortIndicatorShown(True)
        self.gridLayout.addWidget(self.tbl, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(LookupTable)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(LookupTable)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LookupTable.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LookupTable.reject)
        QtCore.QMetaObject.connectSlotsByName(LookupTable)

    def retranslateUi(self, LookupTable):
        LookupTable.setWindowTitle(_translate("LookupTable", "Werte bearbeiten", None))

