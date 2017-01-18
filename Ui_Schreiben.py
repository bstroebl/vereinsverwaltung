# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Ui_Schreiben.ui'
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

class Ui_Schreiben(object):
    def setupUi(self, Schreiben):
        Schreiben.setObjectName(_fromUtf8("Schreiben"))
        Schreiben.setWindowModality(QtCore.Qt.ApplicationModal)
        Schreiben.resize(487, 352)
        self.verticalLayout = QtGui.QVBoxLayout(Schreiben)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Schreiben)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cbxArt = QtGui.QComboBox(Schreiben)
        self.cbxArt.setObjectName(_fromUtf8("cbxArt"))
        self.horizontalLayout.addWidget(self.cbxArt)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_2 = QtGui.QLabel(Schreiben)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.txlAdressaten = QtGui.QLineEdit(Schreiben)
        self.txlAdressaten.setReadOnly(True)
        self.txlAdressaten.setObjectName(_fromUtf8("txlAdressaten"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.txlAdressaten)
        self.label_3 = QtGui.QLabel(Schreiben)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.txlTitel = QtGui.QLineEdit(Schreiben)
        self.txlTitel.setObjectName(_fromUtf8("txlTitel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.txlTitel)
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.dockAnhaenge = QtGui.QDockWidget(Schreiben)
        self.dockAnhaenge.setMaximumSize(QtCore.QSize(300, 96))
        self.dockAnhaenge.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.dockAnhaenge.setObjectName(_fromUtf8("dockAnhaenge"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lstAnhang = QtGui.QListWidget(self.dockWidgetContents_2)
        self.lstAnhang.setMaximumSize(QtCore.QSize(16777215, 55))
        self.lstAnhang.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.lstAnhang.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.lstAnhang.setObjectName(_fromUtf8("lstAnhang"))
        self.gridLayout.addWidget(self.lstAnhang, 0, 0, 1, 1)
        self.dockAnhaenge.setWidget(self.dockWidgetContents_2)
        self.horizontalLayout_2.addWidget(self.dockAnhaenge)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.txtText = QtGui.QTextEdit(Schreiben)
        self.txtText.setObjectName(_fromUtf8("txtText"))
        self.verticalLayout.addWidget(self.txtText)
        self.buttonBox = QtGui.QDialogButtonBox(Schreiben)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Schreiben)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Schreiben.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Schreiben.reject)
        QtCore.QMetaObject.connectSlotsByName(Schreiben)

    def retranslateUi(self, Schreiben):
        Schreiben.setWindowTitle(_translate("Schreiben", "Schreiben", None))
        self.label.setText(_translate("Schreiben", "Art", None))
        self.label_2.setText(_translate("Schreiben", "Adressaten", None))
        self.label_3.setText(_translate("Schreiben", "Betreff", None))
        self.dockAnhaenge.setWindowTitle(_translate("Schreiben", "Anhänge", None))

