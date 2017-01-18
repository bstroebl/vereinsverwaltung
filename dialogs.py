# -*- coding: utf-8 -*-
"""
/***************************************************************************
Mitglied
Mitgliedsverwaltung für PostgreSql
                             -------------------
begin                : 2011-05-26
copyright            : (C) 2011 by Bernhard Stroebl
email                : b.stroebl@stroweb.de
***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui, QtSql, QtXml
from Ui_LookupTable import Ui_LookupTable
from Ui_Verbindung import Ui_Verbindung
from Ui_Schreiben import Ui_Schreiben
from Ui_SMTP import Ui_SMTP
import datamodel
import elixir
import os

class SMTPDialog(QtGui.QDialog):
    '''Dialog zur Verbindungseinstellung SMTP-Server'''

    def __init__(self, settingsList, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_SMTP()
        self.ui.setupUi(self)

        self.ui.host.setText(settingsList[0])
        self.ui.port.setText(settingsList[1])
        self.ui.user.setText(settingsList[2])
        self.ui.password.setText(settingsList[3])
        self.ui.sender.setText(settingsList[4])
        self.ui.chkSSL.setChecked(settingsList[5])
        self.ui.senderName.setText(settingsList[6])

    def accept(self):

        password = self.ui.password.text()

        if not password.isEmpty():
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                "Sicherheitsrisiko", u"Das Passwort wird unverschlüsselt " + \
                u"auf diesem Rechner gespeichert. Speichern Sie das Passwort nur, " + \
                u"wenn Sie sicher sind, dass nur Sie diesen Rechner benutzen.",
                QtGui.QMessageBox.NoButton, self)
            msgBox.addButton(u"Ich kenne das Risiko", QtGui.QMessageBox.AcceptRole)
            msgBox.addButton(u"Nicht Speichern", QtGui.QMessageBox.RejectRole)

            if msgBox.exec_() == QtGui.QMessageBox.RejectRole:
                password = QtCore.QString()

        settings = QtCore.QSettings() #u"Verein", u"Mitgliederverwaltung")
        settings.remove(u"SMTP_Connection")
        settings.beginGroup(u"SMTP_Connection")

        if self.ui.chkSSL.isChecked():
            ssl = "True"
        else:
            ssl= "False"

        settings.setValue("ssl", ssl)
        settings.setValue("host", self.ui.host.text())
        settings.setValue("port", self.ui.port.text())
        settings.setValue("user",self.ui.user.text())
        settings.setValue("password", password)
        settings.setValue("sendername", self.ui.senderName.text())
        settings.setValue("sender", self.ui.sender.text())
        settings.endGroup()

        self.done(1)

class VerbindungsDialog(QtGui.QDialog):
    '''Dialog zur Verbindungseinstellung DB'''

    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Verbindung()
        self.ui.setupUi(self)
        self.initializeValues()

    def initializeValues(self):
        settings = QtCore.QSettings() #u"Verein", u"Mitgliederverwaltung")
        settings.beginGroup(u"DB_Connection")
        qType = settings.value("qtype", "QPSQL").toString() # 2. arg = default if no value
        type = settings.value("type", "PostgreSQL").toString()
        host = settings.value("host", "127.0.0.1").toString()
        dbName = settings.value("database", "").toString()
        port = settings.value("port", "5432").toString()
        user = settings.value("user", "").toString()
        password = settings.value("password", "").toString()
        settings.endGroup()

        self.ui.cbxType.addItem("PostgreSQL", "QPSQL")
        self.ui.cbxType.addItem("MySQL", "QMYSQL")
        self.ui.cbxType.setCurrentIndex(0)

        if type == "MySQL":
            self.ui.cbxType.setCurrentIndex(1)

        self.ui.host.setText(host)
        self.ui.port.setText(port)
        self.ui.database.setText(dbName)
        self.ui.user.setText(user)
        self.ui.password.setText(password)

    def accept(self):

        password = self.ui.password.text()

        if not password.isEmpty():
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                "Sicherheitsrisiko", u"Das Passwort wird unverschlüsselt " + \
                u"auf diesem Rechner gespeichert. Speichern Sie das Passwort nur, " + \
                u"wenn Sie sicher sind, dass nur Sie diesen Rechner benutzen.",
                QtGui.QMessageBox.NoButton, self)
            msgBox.addButton(u"Ich kenne das Risiko", QtGui.QMessageBox.AcceptRole)
            msgBox.addButton(u"Nicht Speichern", QtGui.QMessageBox.RejectRole)

            if msgBox.exec_() == QtGui.QMessageBox.RejectRole:
                password = QtCore.QString()

        settings = QtCore.QSettings() #u"Verein", u"Mitgliederverwaltung")
        settings.remove(u"DB_Connection")
        settings.beginGroup(u"DB_Connection")
        settings.setValue("type", self.ui.cbxType.itemText(self.ui.cbxType.currentIndex()))
        settings.setValue("qtype", self.ui.cbxType.itemData(self.ui.cbxType.currentIndex()))
        settings.setValue("host", self.ui.host.text())
        settings.setValue("database", self.ui.database.text())
        settings.setValue("port", self.ui.port.text())
        settings.setValue("user",self.ui.user.text())
        settings.setValue("password", password)
        settings.endGroup()

        self.done(1)

class TableDialog(QtGui.QDialog):
    '''Dialog mit lookupTable'''

    def __init__(self, tableName, headers, db, successfullySavedMsg = '', parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_LookupTable()
        self.ui.setupUi(self)
        self.tableName = tableName
        self.headers = headers
        self.db = db
        self.successfullySavedMsg = successfullySavedMsg

    def setupModel(self):
        pass

    def findMaxId(self):
        #find last id
        self.maxId = 0
        for i in range(self.model.rowCount()):
            id = self.model.record(i).value(0).toInt()[0]

            if id > self.maxId:
                self.maxId = id

    def setupTable(self):
        #visual stuff
        for i in range(len(self.headers)):
            header = self.headers[i]

            if header:
                self.model.setHeaderData(i, QtCore.Qt.Horizontal, header)
            else:
                self.ui.tbl.setColumnHidden(i, True)

    def setupContextMenu(self):
        self.ui.tbl.contextMenu = QtGui.QMenu(self.ui.tbl)
        add = QtGui.QAction(u"neu", self.ui.tbl.contextMenu)
        self.ui.tbl.contextMenu.addAction(add)
        remove = QtGui.QAction(u"löschen", self.ui.tbl.contextMenu)
        self.ui.tbl.contextMenu.addAction(remove)
        QtCore.QObject.connect(add,
                               QtCore.SIGNAL("triggered()"),
                               self.on_add_triggered)
        QtCore.QObject.connect(remove,
                               QtCore.SIGNAL("triggered()"),
                               self.on_remove_triggered)

    def on_add_triggered(self):
        newRec = self.model.record() # neuen Record _für_ Modell definieren!
        self.maxId = self.maxId + 1
        newRec.setValue(0, self.maxId)
        self.model.insertRecord(0, newRec)
        idx = self.model.index(0, 1)
        self.ui.tbl.setCurrentIndex(idx)
        self.ui.tbl.edit(idx)

    def on_remove_triggered(self):
        selIndex = self.ui.tbl.currentIndex()
        thisRow = selIndex.row()
        self.model.removeRow(thisRow)

    @QtCore.pyqtSlot(QtCore.QPoint, name = "on_tbl_customContextMenuRequested")
    def on_tbl_customContextMenuRequested(self, position):
        clickedIndex = self.ui.tbl.indexAt(position)
        row = clickedIndex.row()
        remove = self.ui.tbl.contextMenu.actions()[1]
        remove.setVisible(clickedIndex.row() >= 0)
        remove.setEnabled(clickedIndex.row() >= 0)
        #row == -1 if no row has been clicked
        self.ui.tbl.contextMenu.resize(self.ui.tbl.contextMenu.sizeHint())
        self.ui.tbl.contextMenu.popup(self.ui.tbl.mapToGlobal(QtCore.QPoint(position)))

    def accept(self):

        if self.model.submitAll():
            if self.successfullySavedMsg != '':
                QtGui.QMessageBox.information(None, u"Änderungen erfolgreich übernommen", \
                    self.successfullySavedMsg)
            self.done(1)
        else:
            QtGui.QMessageBox.warning(None, "Database Error", \
                QtCore.QString("%1").arg(self.model.lastError().text()))


class LookupTableDialog(TableDialog):
    '''Dialog with a simple Lookup-Table; fields: id, value'''

    def __init__(self, tableName, headers, db, successfullySavedMsg, \
                 filter = None, parent = None):
        TableDialog.__init__(self, tableName, headers, db, \
                             successfullySavedMsg, parent)
        self.filter = filter
        self.setupModel()
        self.findMaxId()
        self.setupTable()
        self.setupContextMenu()

    def setupModel(self):
        self.model = QtSql.QSqlTableModel(self.ui.tbl, self.db)
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.setTable(self.tableName)
        self.ui.tbl.setModel(self.model)

        if self.filter:
            self.model.setFilter(self.filter)

        self.model.select()

class LookupTableRelationDialog(TableDialog):
    '''Dialog with a lookup-table that has a relation of its own;
    relation: array 0: int, 1: string, 2: string, 3: string'''

    def __init__(self, tableName, headers, db, relation, successfullySavedMsg, \
                 filter = None, parent = None):
        TableDialog.__init__(self, tableName, headers, db, \
                             successfullySavedMsg, parent)
        self.relation = relation
        self.filter = filter
        self.setupModel()
        self.findMaxId()
        self.setupTable()
        self.setupCbxDelegate()
        self.setupContextMenu()

    def setupModel(self):
        relFldIdx = self.relation[0]
        relTable = self.relation[1]
        targetFld = self.relation[2]
        displayFld = self.relation[3]
        self.model = QtSql.QSqlRelationalTableModel(self.ui.tbl, self.db)
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.setTable(self.tableName)
        self.model.setRelation(relFldIdx, QtSql.QSqlRelation(relTable, targetFld, displayFld))
        self.ui.tbl.setModel(self.model)

        if self.filter:
            self.model.setFilter(filter)

        self.model.select()

    def setupCbxDelegate(self):
        cbxDelegate = QtSql.QSqlRelationalDelegate(self.ui.tbl)
        self.ui.tbl.setItemDelegateForColumn(self.relation[0], cbxDelegate)

class SchreibenDialog(QtGui.QDialog):
    def __init__(self, schreiben, forEdit = True,  parent = None,  noEmail = False):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Schreiben()
        self.ui.setupUi(self)
        self.schreiben = schreiben
        self.forEdit = forEdit
        self.noEmail = noEmail

        self.ui.cbxArt.setEnabled(self.forEdit)
        self.ui.txlAdressaten.setEnabled(self.forEdit)
        self.ui.txlTitel.setEnabled(self.forEdit)
        self.ui.txtText.setReadOnly(not self.forEdit)
        #self.ui.dockAnhaenge.setEnabled(self.forEdit)

        #self.okBtn = self.ui.buttonBox.button(QtGui.QDialogButtonBox.SaveAll)

        if self.forEdit:
            self.ui.lstAnhang.contextMenu = QtGui.QMenu(self.ui.lstAnhang)
            self.addAnhang = QtGui.QAction(u"Anhang hinzufügen",
                                        self.ui.lstAnhang.contextMenu)
            self.ui.lstAnhang.contextMenu.addAction(self.addAnhang)
            self.removeAnhang = QtGui.QAction(u"Anhang entfernen",
                                           self.ui.lstAnhang.contextMenu)
            self.ui.lstAnhang.contextMenu.addAction(self.removeAnhang)
            QtCore.QObject.connect(self.addAnhang,
                               QtCore.SIGNAL("triggered()"),
                               self.on_addAnhang_triggered)
            QtCore.QObject.connect(self.removeAnhang,
                               QtCore.SIGNAL("triggered()"),
                               self.on_removeAnhang_triggered)

        self.initializeValues()

    def cbxValueFromText(self, cbx, thisText):
        for i in range( cbx.count() ):
            if cbx.itemText( i ) == thisText:
                cbx.setCurrentIndex( i )
                break

    def initializeValues(self):
        for schreibenArt in datamodel.Schreibenart.query.order_by(\
                    datamodel.Schreibenart.schreibenart).all():

            if not (schreibenArt.schreibenart == "Email" and self.noEmail):
                self.ui.cbxArt.addItem(schreibenArt.schreibenart)

        if self.schreiben.art:
            self.cbxValueFromText(self.ui.cbxArt, self.schreiben.art.schreibenart)
        else:
            self.ui.cbxArt.setCurrentIndex(0)

        adressaten = QtCore.QString()

        for mitglied in self.schreiben.mitglieder:

            if adressaten != "":
                adressaten.append(", " + mitglied.mitgliedsname + " (" + str(mitglied.mitgliedsnummer) + ")")
            else:
                adressaten = QtCore.QString(mitglied.mitgliedsname + " (" + str(mitglied.mitgliedsnummer) + ")")

        self.ui.txlAdressaten.setText(adressaten)

        if self.schreiben.titel:
            self.ui.txlTitel.setText(self.schreiben.titel)

        if self.schreiben.text:

            if self.schreiben.art == "Brief":
                self.ui.txtText.setHtml(QtCore.QString(self.schreiben.text))
            else:
                self.ui.txtText.setText(QtCore.QString(self.schreiben.text))

        self.ui.lstAnhang.clear()

        for anhang in self.schreiben.anhaenge:
            self.showAnhang(anhang.pfad)

    #Slots
    def on_addAnhang_triggered(self):
        lastPath = None
        settings = QtCore.QSettings()
        settings.beginGroup(u"Schreiben")

        if len(settings.childKeys()) > 0:
            lastPath = settings.value("lastPath").toString()

        settings.endGroup()

        if not lastPath:
            lastPath = ""

        files = QtGui.QFileDialog.getOpenFileNames(self,
                         u"Anhänge auswählen",
                         str(lastPath))

        if len(files) > 0:
            for aFile in files:
                self.showAnhang(str(aFile))

            # last Path schreiben
            lastPath = os.path.dirname(str(aFile))
            settings.beginGroup(u"Schreiben")
            settings.setValue("lastPath",  lastPath)
            settings.endGroup()

    def on_removeAnhang_triggered(self):
        for anItem in self.ui.lstAnhang.selectedItems():
            anItem.setHidden(True)

    @QtCore.pyqtSlot(QtGui.QListWidgetItem, name = "on_lstAnhang_itemDoubleClicked")
    def on_lstAnhang_itemDoubleClicked(self,  thisItem):
        fileName = str(thisItem.toolTip())
        if os.path.exists(fileName):
            if os.name == 'nt': # Window$
                os.startfile(fileName)
            elif os.name == 'posix': # e.g. linux
                subprocess.call(['xdg-open', fileName])
        else:
            QtGui.QMessageBox.warning(None,  "Datei nicht gefunden",
                                      u"Die Datei " + thisPath + u"konnte nicht geunden werden!")

    @QtCore.pyqtSlot(QtCore.QString, name = "on_cbxArt_currentIndexChanged")
    def on_cbxArt_currentIndexChanged(self, thisText):

        if thisText == "Email":
            self.ui.dockAnhaenge.show()
        else:
            self.ui.dockAnhaenge.close()

    @QtCore.pyqtSlot(QtCore.QPoint, name = "on_lstAnhang_customContextMenuRequested")
    def on_lstAnhang_customContextMenuRequested(self, position):
        if self.forEdit:
            thisItem = self.ui.lstAnhang.itemAt(position)
            self.removeAnhang.setVisible(thisItem != None)
            self.ui.lstAnhang.contextMenu.resize(self.ui.lstAnhang.contextMenu.sizeHint())
            self.ui.lstAnhang.contextMenu.popup(self.ui.lstAnhang.mapToGlobal(QtCore.QPoint(position)))

    def accept(self):
        self.schreiben.titel = unicode(self.ui.txlTitel.text())
        thisSchreibenart = unicode(self.ui.cbxArt.currentText())

        if thisSchreibenart == "Email":
            text = self.ui.txtText.toPlainText()
        else:
            text = self.ui.txtText.toHtml()

        self.schreiben.text = unicode(text)
        schreibenArt = datamodel.Schreibenart.get_by(schreibenart = thisSchreibenart)
        self.schreiben.art = schreibenArt

        for aRow in range(self.ui.lstAnhang.count()):
            anItem = self.ui.lstAnhang.item(aRow)

            if not anItem.isHidden():
                anhang = datamodel.Schreibenanhang()
                thisPath = str(anItem.toolTip())
                anhang.pfad = thisPath
                anhang.schreiben = self.schreiben

        self.done(1)

    def showAnhang(self, pfad):
        newItem = QtGui.QListWidgetItem(os.path.basename(pfad))
        self.ui.lstAnhang.addItem(newItem)
        newItem.setToolTip(pfad)


