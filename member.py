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
from datetime import date, datetime
from Ui_Mitglied import Ui_Mitglied
from Ui_MitgliedNatuerlich import Ui_MitgliedNatuerlich
from Ui_MitgliedJuristisch import Ui_MitgliedJuristisch
from dialogs import LookupTableDialog, SchreibenDialog
import resources_rc
import datamodel
import elixir
from sqlalchemy import and_

class RadioButtonDelegate(QtGui.QStyledItemDelegate):
    '''Delegate, zur Eingabe von 0 = Falsch 1 = Wahr -
    Werten über RadioButton in TableViews'''

    def __init__(self, parent = None):
        QtGui.QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = QtGui.QRadioButton(parent)
        return editor

    def setEditorData(self, editor, index):
        bol = bool(index.model().data(index, QtCore.Qt.DisplayRole))
        editor.setChecked(bol)

    def setModelData(self, editor, model, index):
        model.setData(index, QtCore.QVariant(int(editor.isChecked())))

class CheckBoxDelegate(QtGui.QStyledItemDelegate):
    '''Delegate, zur Eingabe von 0 = Falsch 1 = Wahr -
    Werten über RadioButton in TableViews'''

    def __init__(self, parent = None):
        QtGui.QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = QtGui.QCheckBox(parent)
        return editor

    def setEditorData(self, editor, index):
        bol = bool(index.model().data(index, QtCore.Qt.DisplayRole))
        editor.setChecked(bol)

    def setModelData(self, editor, model, index):
        model.setData(index, QtCore.QVariant(int(editor.isChecked())))


class DatumDelegate(QtGui.QStyledItemDelegate):
    '''Delegate, zur Datumseingabe in TableViews'''

    def __init__(self, parent = None):
        QtGui.QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = QtGui.QDateEdit(parent)
        editor.setDisplayFormat("dd.MM.yyyy")
        editor.setMaximumDate(QtCore.QDate.currentDate())
        editor.setCalendarPopup(True)
        return editor

    def setEditorData(self, editor, index):
        text = index.model().data(index, QtCore.Qt.DisplayRole).toDate()
        editor.setDate(text)

    def setModelData(self, editor, model, index):
        model.setData(index, QtCore.QVariant(editor.date()))

class MemberData(QtGui.QWidget):
    ''' aus DB gelesene Daten werden in Klassenattributen gehalten,
    erst beim Speichern werden die Eingabefelder ausgelesen
    Kontaktdaten und Zahlungen werden über ein SQLModel verwaltet'''

    def __init__(self, db, application, parentWidget = 0, memberId = -9999):
        QtGui.QWidget.__init__(self, parentWidget)

        self.ui = Ui_Mitglied()
        self.ui.setupUi(self)
        self.db = db
        self.application = application
        self.tabWidget = self.application.ui.tabMitglied
        self.memberId = memberId
        #self.enums = enums

        # die uis für natürliches und juristisches Mitglied einfügen
        self.naturalMember = NaturalMember(self.ui.pgPerson, self.memberId)
        self.legalMember = LegalMember(self.ui.pgPerson, self.memberId)
        self.ui.pgPerson.layout().addWidget(self.naturalMember)
        self.ui.pgPerson.layout().addWidget(self.legalMember)

        # QButtonBox-Buttons auf Klassenattribute legen
        bb = self.ui.buttonBox
        self.saveBtn = bb.button(QtGui.QDialogButtonBox.Save)
        self.saveBtn.setEnabled(False)
        self.resetBtn = bb.button(QtGui.QDialogButtonBox.Reset)
        self.resetBtn.setEnabled(False)
        self.closeBtn = bb.button(QtGui.QDialogButtonBox.Close)

        #elixir-Session
        elixir.metadata.bind = "sqlite:///" + self.application.dbfile
        elixir.metadata.bind.echo = True
        elixir.setup_all()

        #context menu
        self.ui.tblTelefon.contextMenu = QtGui.QMenu(self.ui.tblTelefon)
        self.addTelefon = QtGui.QAction(u"Nummer hinzufügen",
                                        self.ui.tblTelefon.contextMenu)
        self.ui.tblTelefon.contextMenu.addAction(self.addTelefon)
        self.removeTelefon = QtGui.QAction(u"Nummer löschen",
                                           self.ui.tblTelefon.contextMenu)
        self.ui.tblTelefon.contextMenu.addAction(self.removeTelefon)

        self.ui.tblEmail.contextMenu = QtGui.QMenu(self.ui.tblEmail)
        self.addEmail = QtGui.QAction(u"Email hinzufügen",
                                      self.ui.tblEmail.contextMenu)
        self.ui.tblEmail.contextMenu.addAction(self.addEmail)
        self.removeEmail = QtGui.QAction(u"Email löschen",
                                         self.ui.tblEmail.contextMenu)
        self.ui.tblEmail.contextMenu.addAction(self.removeEmail)
        self.showEmailErrors = QtGui.QAction(u"Fehler anzeigen",
                                         self.ui.tblEmail.contextMenu)
        self.ui.tblEmail.contextMenu.addAction(self.showEmailErrors)

        self.ui.tblZahlungen.contextMenu = QtGui.QMenu(self.ui.tblZahlungen)
        self.addZahlung = QtGui.QAction(u"Neue Zahlung",
                                      self.ui.tblZahlungen.contextMenu)
        self.ui.tblZahlungen.contextMenu.addAction(self.addZahlung)

        self.initializeValues()
        self.connectSlots()


    def prepareCbxValues(self):
        anredeList = QtCore.QStringList()
        for anrede in datamodel.Anrede.query.order_by(\
               datamodel.Anrede.anrede).all():
            anredeList.append(anrede.anrede)

        austrittsgrundList = QtCore.QStringList()
        for austrittsgrund in datamodel.Austrittsgrund.query.all():
            austrittsgrundList.append(austrittsgrund.austrittsgrund)

        beitragsgruppeList = QtCore.QStringList()
        for beitragsgruppe in datamodel.Beitragsgruppe.query.order_by(\
                datamodel.Beitragsgruppe.beitragsgruppe).all():
            beitragsgruppeList.append(beitragsgruppe.beitragsgruppe)

        mitgliedsgruppeList = QtCore.QStringList()
        for mitgliedsgruppe in datamodel.Mitgliedsgruppe.query.order_by(\
                datamodel.Mitgliedsgruppe.mitgliedsgruppe).all():
            mitgliedsgruppeList.append(mitgliedsgruppe.mitgliedsgruppe)

        ortList = QtCore.QStringList()
        for ort in datamodel.Ort.query.order_by(\
                datamodel.Ort.plz, datamodel.Ort.ort).all():
            ortList.append(ort.plz + " " + ort.ort)

        schreibenartList = QtCore.QStringList()
        for schreibenart in datamodel.Schreibenart.query.order_by(\
                datamodel.Schreibenart.schreibenart).all():
            schreibenartList.append(schreibenart.schreibenart)

        zahlungsartList = QtCore.QStringList()
        for zahlungsart in datamodel.Zahlungsart.query.order_by(\
                datamodel.Zahlungsart.zahlungsart).all():
            zahlungsartList.append(zahlungsart.zahlungsart)

        zahlweiseList = QtCore.QStringList()
        for zahlweise in datamodel.Zahlweise.query.order_by(\
                datamodel.Zahlweise.zahlweise).all():
            zahlweiseList.append(zahlweise.zahlweise)

        landList = QtCore.QStringList()
        for land in datamodel.Land.query.order_by(\
                datamodel.Land.land).all():
            landList.append(land.land)

        self.enums = {\
            'Anrede': anredeList,
            'Austrittsgrund': austrittsgrundList,
            'Beitragsgruppe': beitragsgruppeList,
            'Land': landList,
            'Mitgliedsgruppe': mitgliedsgruppeList,
            'Ort': ortList,
            'Schreibenart': schreibenartList,
            'Zahlungsart': zahlungsartList,
            'Zahlweise': zahlweiseList \
        }

    def initializeValues(self):

        self.noChanges = True
        self.prepareCbxValues()
        self.naturalMember.ui.cbxAnrede.addItems(self.enums['Anrede'])
        self.ui.cbxAustrittsgrund.addItems(self.enums['Austrittsgrund'])
        self.ui.cbxBeitragsgruppe.addItems(self.enums['Beitragsgruppe'])
        self.ui.cbxKategorie.addItems(self.enums['Mitgliedsgruppe'])
        self.ui.cbxOrt.addItems(self.enums['Ort'])
        self.ui.cbxLand.addItems(self.enums['Land'])
        self.ui.cbxZahlungsart.addItems(self.enums['Zahlungsart'])
        self.ui.cbxZahlweise.addItems(self.enums['Zahlweise'])

        horizontalHeaders = QtCore.QStringList(QtCore.QString('Datum'))
        horizontalHeaders.append(QtCore.QString('Betreff'))
        horizontalHeaders.append(QtCore.QString('Art'))
        self.ui.tblSchreiben.horizontalHeader().setVisible(True)
        self.ui.tblSchreiben.setHorizontalHeaderLabels(horizontalHeaders)

        #set defaultValues
        self.hauptmitgliedId = None
        self.ui.dateAustrittsDatum.setDate(QtCore.QDate())

        #validators
        hnrValidator = QtGui.QIntValidator(1, 10000, self.ui.txlHnr)
        self.ui.txlHnr.setValidator(hnrValidator)

        self.setMemberValues()

        #visibility
        self.ui.cbxAustrittsgrund.setVisible(False)

    def fillEmail(self):
        emailModel = QtSql.QSqlRelationalTableModel(self.ui.tblEmail, self.db)
        emailModel.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        emailModel.setTable("emailadresse")
        emailModel.setRelation(3, QtSql.QSqlRelation("hinweis_email", "id", "hinweis"))
        filter = QtCore.QString("mitglied_id = " )
        filter.append(str(self.memberId))
        self.ui.tblEmail.setModel(emailModel)
        emailModel.setFilter(filter)
        emailModel.select()

        #visual stuff
        self.ui.tblEmail.setColumnHidden(0, True) # id
        self.ui.tblEmail.setColumnHidden(1, True) # mitglied_id
        emailModel.setHeaderData(2, QtCore.Qt.Horizontal, u"Email")
        emailModel.setHeaderData(3, QtCore.Qt.Horizontal, u"Hinweis")

        if emailModel.rowCount() > 0:
            self.ui.tblEmail.resizeColumnToContents(2)

        #editDelegate, here comboBox
        hinweisDelegate = QtSql.QSqlRelationalDelegate(self.ui.tblEmail)
        self.ui.tblEmail.setItemDelegateForColumn(3, hinweisDelegate)

        QtCore.QObject.connect(emailModel,
                               QtCore.SIGNAL("beforeInsert(QSqlRecord&)"),
                               self.beforeInsertRec)

    def fillTelefon(self):
        model = QtSql.QSqlRelationalTableModel(self.ui.tblTelefon, self.db)
        model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model.setTable("telefonfax")
        model.setRelation(3, QtSql.QSqlRelation("hinweis_telefonfax", "id", "hinweis"))
        filter = QtCore.QString("mitglied_id = " )
        filter.append(str(self.memberId))
        self.ui.tblTelefon.setModel(model)
        model.setFilter(filter)
        model.select()

        #visual stuff
        self.ui.tblTelefon.setColumnHidden(0, True) # id
        self.ui.tblTelefon.setColumnHidden(1, True) # mitglied_id
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Nummer")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Hinweis")

        if model.rowCount() > 0:
            self.ui.tblTelefon.resizeColumnToContents(2)

        #editDelegate, here comboBox
        hinweisDelegate = QtSql.QSqlRelationalDelegate(self.ui.tblTelefon)
        self.ui.tblTelefon.setItemDelegateForColumn(3, hinweisDelegate)

        QtCore.QObject.connect(model,
                               QtCore.SIGNAL("beforeInsert(QSqlRecord&)"),
                               self.beforeInsertRec)

    def fillZahlungen(self):
        model = QtSql.QSqlRelationalTableModel(self.ui.tblZahlungen, self.db)
        model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model.setTable("zahlung")
        model.setRelation(4, QtSql.QSqlRelation("hinweis_zahlung", "id", "hinweis"))
        filter = QtCore.QString("mitglied_id = " )
        filter.append(str(self.memberId))
        self.ui.tblZahlungen.setModel(model)
        model.setFilter(filter)
        model.select()

        #visual stuff
        self.ui.tblZahlungen.setColumnHidden(0, True) # id
        self.ui.tblZahlungen.setColumnHidden(1, True) # mitglied_id
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Betrag")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Datum")
        model.setHeaderData(4, QtCore.Qt.Horizontal, u"Hinweis")

        #if model.rowCount() > 0:
        #    self.ui.tblZahlungen.resizeColumnsToContents()

        #editDelegates
        datumDelegate = DatumDelegate(self.ui.tblZahlungen)
        self.ui.tblZahlungen.setItemDelegateForColumn(3, datumDelegate)
        hinweisDelegate = QtSql.QSqlRelationalDelegate(self.ui.tblZahlungen)
        self.ui.tblZahlungen.setItemDelegateForColumn(4, hinweisDelegate)

        #loc = self.locale()
        #QtGui.QMessageBox.information(None, "", loc.dateFormat())

        self.newZahlungRows = 0
        QtCore.QObject.connect(model,
                               QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"),
                               self.on_zahlungen_dataChanged)

        QtCore.QObject.connect(model,
                               QtCore.SIGNAL("beforeInsert(QSqlRecord&)"),
                               self.beforeInsertRec)

    def fillSchreiben(self):

        if self.memberId > 0: # nur bereits gespeicherte Mitglieder können Schreiben haben
            self.ui.tblSchreiben.clearContents()
            self.ui.tblSchreiben.setRowCount(0)

            for schreiben in self.mitglied.schreiben:
                thisRow = self.ui.tblSchreiben.rowCount()
                # identical with index of row to be appended as row indices are 0 based
                self.ui.tblSchreiben.setRowCount(thisRow + 1) #add a row
                schreibenItem = QtGui.QTableWidgetItem(str(schreiben.erzeugt))
                schreibenItem.schreiben = schreiben
                self.ui.tblSchreiben.setItem(thisRow, 0,
                    schreibenItem)
                self.ui.tblSchreiben.setItem(thisRow, 1,
                    QtGui.QTableWidgetItem(schreiben.titel))
                self.ui.tblSchreiben.setItem(thisRow, 2,
                    QtGui.QTableWidgetItem(schreiben.art.schreibenart))

    def connectSlots(self):

        for cbx in [self.ui.cbxOrt, self.ui.cbxKategorie, self.ui.cbxBeitragsgruppe,
                    self.ui.cbxZahlungsart, self.ui.cbxBeitragsgruppe,
                    self.naturalMember.ui.cbxAnrede]:
            QtCore.QObject.connect(cbx,
                                   QtCore.SIGNAL("currentIndexChanged(int)"),
                                   self.cbxHasChanged)

        for txl in [self.naturalMember.ui.txlTitel, self.naturalMember.ui.txlVorname,
                    self.naturalMember.ui.txlName, self.naturalMember.ui.txlNamenszusatz,
                    self.naturalMember.ui.txlBeruf,  self.naturalMember.ui.txlHauptmitglied,
                    self.legalMember.ui.txlName, self.legalMember.ui.txlAnsprechpartner,
                    self.ui.txlStrasse, self.ui.txlHnr, self.ui.txlHnrZusatz,
                    self.ui.txlAdresszusatz, self.ui.txlIndividuellerBeitrag,
                    self.ui.txlKontonummer, self.ui.txlBlz, self.ui.txlInstitut,
                    self.ui.txlKontoInhaber,  self.ui.txlIban,  self.ui.txlBic]:
            QtCore.QObject.connect(txl,
                                   QtCore.SIGNAL("editingFinished()"),
                                   self.txlHasChanged)

        for dat in [self.naturalMember.ui.dateGeburtsdatum, self.ui.dateEintrittsDatum,
                    self.ui.dateAustrittsDatum]:
            QtCore.QObject.connect(dat,
                                   QtCore.SIGNAL("dateChanged(QDate)"),
                                   self.changed)

        QtCore.QObject.connect(self.saveBtn,
                               QtCore.SIGNAL("clicked()"),
                               self.on_saveBtn_clicked)
        QtCore.QObject.connect(self.resetBtn,
                               QtCore.SIGNAL("clicked()"),
                               self.on_resetBtn_clicked)
        QtCore.QObject.connect(self.closeBtn,
                               QtCore.SIGNAL("clicked()"),
                               self.on_closeBtn_clicked)

        #contextMenus
        QtCore.QObject.connect(self.addTelefon,
                               QtCore.SIGNAL("triggered()"),
                               self.on_addTelefon_triggered)
        QtCore.QObject.connect(self.removeTelefon,
                               QtCore.SIGNAL("triggered()"),
                               self.on_removeTelefon_triggered)
        QtCore.QObject.connect(self.addEmail,
                               QtCore.SIGNAL("triggered()"),
                               self.on_addEmail_triggered)
        QtCore.QObject.connect(self.removeEmail,
                               QtCore.SIGNAL("triggered()"),
                               self.on_removeEmail_triggered)
        QtCore.QObject.connect(self.showEmailErrors,
                               QtCore.SIGNAL("triggered()"),
                               self.on_showEmailErrors_triggered)
        QtCore.QObject.connect(self.addZahlung,
                               QtCore.SIGNAL("triggered()"),
                               self.on_addZahlung_triggered)

    #SLOTS
    def on_saveBtn_clicked(self):

        if self.saveToDb(): # creates a memberId on INSERT
            displayname = self.mitglied.mitgliedsname

            if self.mitglied.vorname:
                displayname = self.mitglied.vorname + " " + displayname

            self.tabWidget.setTabText(self.tabWidget.currentIndex(), \
                                      QtCore.QString(displayname))

            if self.memberId < 0:
                self.memberId = self.mitglied.mitgliedsnummer
                self.tabWidget.setObjectName(QtCore.QString(self.memberId))
                self.fillEmail()
                self.fillTelefon()
                self.fillZahlungen()
                self.fillSchreiben()

            self.application.ui.tblMitglieder.model().select()
            self.hasNoChanges()

    @QtCore.pyqtSlot(QtCore.QString, name = "on_cbxBeitragsgruppe_currentIndexChanged")
    def on_cbxBeitragsgruppe_currentIndexChanged(self, thisBeitragsgruppe):
        beitragsgruppe = datamodel.Beitragsgruppe.query.filter_by( \
                          beitragsgruppe = unicode(thisBeitragsgruppe)).one()
        self.ui.txlBeitrag.setText(str(beitragsgruppe.beitrag_nach_satzung))

    def on_closeBtn_clicked(self):
        if self.on_memberTabCloseRequested():
            self.tabWidget.removeTab(self.tabWidget.currentIndex())

    def on_resetBtn_clicked(self):
        self.setMemberValues()

        for tbl in [self.ui.tblEmail, self.ui.tblTelefon, self.ui.tblZahlungen]:
            tbl.model().select()

        self.hasNoChanges()

    def on_addTelefon_triggered(self):
        model = self.ui.tblTelefon.model()
        newRec = model.record() # neuen Record _für_ Modell definieren!
        newRec.setValue(1, self.memberId)
        newRec.setValue(3, QtCore.QVariant(1))
        model.insertRecord(0, newRec)
        idx = model.index(0, 2)
        self.ui.tblTelefon.setCurrentIndex(idx)
        self.ui.tblTelefon.edit(idx)
        self.changed()

    def on_removeTelefon_triggered(self):
        model =  self.ui.tblTelefon.model()
        selIndex = self.ui.tblTelefon.currentIndex()
        thisRow = selIndex.row()
        rec = model.record(thisRow)
        rec.setValue(2, u"gelöscht")
        model.setRecord(thisRow, rec)
        model.removeRow(thisRow)
        self.changed()

    def on_addEmail_triggered(self):
        model = self.ui.tblEmail.model()
        newRec = model.record() # neuen Record für Modell definieren!
        newRec.setValue(1, self.memberId)
        newRec.setValue(3, QtCore.QVariant(1))
        model.insertRecord(0, newRec)
        idx = model.index(0, 2)
        self.ui.tblEmail.setCurrentIndex(idx)
        self.ui.tblEmail.edit(idx)
        self.changed()

    def on_removeEmail_triggered(self):
        model =  self.ui.tblEmail.model()
        selIndex = self.ui.tblEmail.currentIndex()
        thisRow = selIndex.row()
        rec = model.record(thisRow)
        rec.setValue(2, u"gelöscht")
        model.setRecord(thisRow, rec)
        model.removeRow(thisRow)
        self.changed()

    def on_showEmailErrors_triggered(self):
        model = self.ui.tblEmail.model()
        selIndex = self.ui.tblEmail.currentIndex()
        thisRow = selIndex.row()
        rec = model.record(thisRow)
        emailId = rec.value(0)
        filter = QtCore.QString("email_id = " + str(emailId))
        dlg = LookupTableDialog("emailfehler", [None, "Fehler", "Datum", None],
                                self.db, "", filter, self)
        dlg.show()
        result = dlg.exec_()

    def on_addZahlung_triggered(self):
        model = self.ui.tblZahlungen.model()
        newRec = model.record() # neuen Record für Modell definieren!
        newRec.setValue(1, self.memberId)
        newRec.setValue(3, QtCore.QVariant(QtCore.QDate.currentDate()))
        newRec.setValue(4, QtCore.QVariant(1))
        model.insertRecord(0, newRec)
        idx = model.index(0, 2)
        self.ui.tblZahlungen.setCurrentIndex(idx)
        self.ui.tblZahlungen.edit(idx)
        self.newZahlungRows += 1
        self.changed()

    def beforeInsertRec(self,  newRec):
        newRec.setGenerated("id", False) # muß sein für Qt 4.8
        #https://bugreports.qt-project.org/browse/QTBUG-23592?page=com.atlassian.jira.plugin.system.issuetabpanels:all-tabpanel
        # http://stackoverflow.com/questions/10147343/qsqlrecord-sets-column-with-default-value-to-null-in-query

    @QtCore.pyqtSlot(bool)
    def on_radOrtCbx_toggled(self, isChecked):
        self.ui.cbxOrt.setEnabled(isChecked)

        for ctrl in [self.ui.labPlz, self.ui.labOrt, self.ui.labLand, \
                     self.ui.txlPlz, self.ui.txlOrt, self.ui.cbxLand]:
            ctrl.setEnabled(not isChecked)

    @QtCore.pyqtSlot()
    def on_btnAustrittHeute_clicked(self):
        self.manageAustrittsdatum(QtCore.QDate.currentDate())

    @QtCore.pyqtSlot()
    def on_btnEinzugsermaechtigungHeute_clicked(self):
        self.ui.dateEinzugsermaechtigung.setDate(QtCore.QDate.currentDate())

    @QtCore.pyqtSlot(QtCore.QPoint, name = "on_tblEmail_customContextMenuRequested")
    def on_tblEmail_customContextMenuRequested(self, position):
        clickedIndex = self.ui.tblEmail.indexAt(position)
        self.addEmail.setVisible(True)
        row = clickedIndex.row()
        #row == -1 if no row has been clicked
        self.removeEmail.setVisible(row >= 0)
        self.removeEmail.setEnabled(row >= 0)
        self.showEmailErrors.setVisible(row >= 0)
        self.showEmailErrors.setEnabled(row >= 0)

        if row >= 0:
            model = self.ui.tblEmail.model()
            rec = model.record(row)
            emailId = rec.value(0).toInt()[0]
            self.showEmailErrors.setVisible(emailId >= 0)
            self.showEmailErrors.setEnabled(emailId >= 0)

            if emailId > 0: # nur bereits gespeicherte Emailadressen können Fehler haben
                email = datamodel.EmailAdresse.query.filter_by(id=emailId).first()
                numErrors = len(email.fehler)
                self.showEmailErrors.setVisible(numErrors > 0)
                self.showEmailErrors.setEnabled(numErrors > 0)

        self.ui.tblEmail.contextMenu.resize(self.ui.tblEmail.contextMenu.sizeHint())
        self.ui.tblEmail.contextMenu.popup(self.ui.tblEmail.mapToGlobal(QtCore.QPoint(position)))

    @QtCore.pyqtSlot(QtCore.QModelIndex, name = "on_tblEmail_doubleClicked")
    def on_tblEmail_doubleClicked(self, clickedIndex):
        self.changed()

    @QtCore.pyqtSlot(QtCore.QPoint, name = "on_tblTelefon_customContextMenuRequested")
    def on_tblTelefon_customContextMenuRequested(self, position):
        clickedIndex = self.ui.tblTelefon.indexAt(position)
        row = clickedIndex.row()
        self.removeTelefon.setVisible(clickedIndex.row() >= 0)
        self.removeTelefon.setEnabled(clickedIndex.row() >= 0)
        #row == -1 if no row has been clicked

        self.ui.tblTelefon.contextMenu.resize(self.ui.tblTelefon.contextMenu.sizeHint())
        self.ui.tblTelefon.contextMenu.popup(self.ui.tblTelefon.mapToGlobal(QtCore.QPoint(position)))

    @QtCore.pyqtSlot(QtCore.QModelIndex, name = "on_tblTelefon_doubleClicked")
    def on_tblTelefon_doubleClicked(self, clickedIndex):
        self.changed()

    @QtCore.pyqtSlot(name = "on_txlBlz_editingFinished")
    def on_txlBlz_editingFinished(self):
        pass

    @QtCore.pyqtSlot(int, int, name = "on_tblSchreiben_cellDoubleClicked")
    def on_tblSchreiben_cellDoubleClicked(self, thisRow, thisColumn):
        schreibenItem = self.ui.tblSchreiben.item(thisRow, 0)
        dlg = SchreibenDialog(schreibenItem.schreiben, False)
        dlg.showMaximized()
        result = dlg.exec_()

    @QtCore.pyqtSlot(QtCore.QPoint, name = "on_tblZahlungen_customContextMenuRequested")
    def on_tblZahlungen_customContextMenuRequested(self, position):
        clickedIndex = self.ui.tblZahlungen.indexAt(position)

        self.ui.tblZahlungen.contextMenu.resize(self.ui.tblZahlungen.contextMenu.sizeHint())
        self.ui.tblZahlungen.contextMenu.popup(self.ui.tblZahlungen.mapToGlobal(QtCore.QPoint(position)))

    def on_zahlungen_dataChanged(self, fromIdx, toIdx):

        thisRow = fromIdx.row()
        if thisRow <= self.newZahlungRows:
            self.changed()
        else:
            QtGui.QMessageBox.warning(None, u"Keine Änderung möglich ",
                                  u"Zahlungen können nicht geändert werden!")

    @QtCore.pyqtSlot(name = "on_memberTabCloseRequested")
    def on_memberTabCloseRequested(self):
        #QtGui.QMessageBox.information(None,"", "on_memberTabCloseRequested")
        if self.saveBtn.isEnabled():
            reply = QtGui.QMessageBox.question(None, u"Änderungen nicht gespeichert",
                        u"Sollen die Änderungen vor dem Schließen gespeichert werden?",
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,  QtGui.QMessageBox.Yes)

            if reply == QtGui.QMessageBox.Yes:
                success = self.saveToDb()
                elixir.session.close()
                return success
            else:
                for tbl in [self.ui.tblEmail, self.ui.tblTelefon, self.ui.tblZahlungen]:
                    model = tbl.model()
                    model.revertAll()
                elixir.session.close()
                return True
        else:
            elixir.session.close()
            return True

    @QtCore.pyqtSlot()
    def on_radNatuerlichePerson_clicked(self):
        self.legalMember.hide()
        self.naturalMember.show()
       # self.ui.radNatuerlichePerson.setVisible(False)
        #self.ui.radJuristischePerson.setVisible(False)
        self.isNaturalMember = True

    @QtCore.pyqtSlot()
    def on_radJuristischePerson_clicked(self):
        self.naturalMember.hide()
        self.legalMember.show()
        #self.ui.radNatuerlichePerson.setVisible(False)
        #self.ui.radJuristischePerson.setVisible(False)
        self.isNaturalMember = False

    def cbxValueFromInt(self, cbx, thisInt):
        for i in range(cbx.count()):
            if cbx.itemData(i) == thisInt:
                cbx.setCurrentIndex(i)
                break

    def cbxValueFromString(self, cbx, thisString):
        for i in range(cbx.count()):
            if cbx.itemText(i) == thisString:
                cbx.setCurrentIndex(i)
                break

    def cbxHasChanged(self, thisIdx):
        self.changed()

    def txlHasChanged(self):
        self.changed()

    def changed(self):
        '''function to be called if anything has changed'''
        self.saveBtn.setEnabled(self.mandatoryFieldsFilled())

        if self.noChanges:
            self.resetBtn.setEnabled(self.memberId >= 0)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/identity_notsaved.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.tabWidget.setTabIcon(self.tabWidget.currentIndex(), icon)
            noChanges = False

    def hasNoChanges(self):
        self.saveBtn.setEnabled(False)
        self.resetBtn.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/identity_ok.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.setTabIcon(self.tabWidget.currentIndex(), icon)
        self.noChanges = True

    def mandatoryFieldsFilled(self):
        '''check if relevant fields have entries'''

        if self.isNaturalMember:
            retValue = (not self.naturalMember.ui.txlName.text().isEmpty()) and \
                       (not self.naturalMember.ui.txlVorname.text().isEmpty())
        else:
            retValue = (not self.legalMember.ui.txlName.text().isEmpty()) and \
                       (not self.legalMember.ui.txlAnsprechpartner.text().isEmpty())

        if retValue:
            if self.ui.radOrtCbx.isChecked():
                retValue = not self.ui.cbxOrt.currentText().isEmpty()
            else:
                retValue = (not self.ui.txlOrt.text().isEmpty()) and \
                       (not self.ui.txlPlz.text().isEmpty()) and \
                       (not self.ui.cbxLand.currentText().isEmpty())

            if retValue:
                retValue = (not self.ui.txlStrasse.text().isEmpty()) and \
                           (not self.ui.txlHnr.text().isEmpty())

                if retValue:
                    retValue = (not self.ui.cbxKategorie.currentText().isEmpty()) and \
                           (not self.ui.cbxBeitragsgruppe.currentText().isEmpty()) and \
                           (not self.ui.txlBeitrag.text().isEmpty()) and \
                           (not self.ui.cbxZahlungsart.currentText().isEmpty()) and \
                           (not self.ui.cbxZahlweise.currentText().isEmpty())

                    if retValue and self.ui.cbxZahlungsart.currentText() == 'Bankeinzug':
                        retValue =  \
                               (not self.ui.txlBic.text().isEmpty()) and \
                               (not self.ui.txlIban.text().isEmpty()) and \
                               (not self.ui.txlKontoInhaber.text().isEmpty()) and \
                               (self.ui.dateEinzugsermaechtigung.date() != QtCore.QDate())

        return retValue

    def intToString(self, thisInt):
        '''return thisInt as QString, if thisInt is None return an empty QString'''

        if thisInt:
            return QtCore.QString(str(thisInt))
        else:
            return QtCore.QString()

    def qDateToDate(self, qDate):
        ''' return a QDate as Python date-object'''

        return date(qDate.year(), qDate.month(), qDate.day())

    def noneOrInt(self, v):
        '''return None if QVariant v isNull, else return as int'''

        if v.isNull():
            return None
        else:
            if v.canConvert(QtCore.QVariant.Int):
                return int(v.toInt()[0])
            else:
                return None

    def nonify(self, txl):
        '''return string or None if QLineEdit txl is empty'''

        result = txl.text()

        if result.isEmpty():
            return None
        else:
            return unicode(result)

    def nonifyInt(self, txl):
        '''return int or None if QLineEdit txl is empty'''

        result = txl.text()

        if result.isEmpty():
           return None
        else:
            result = QtCore.QVariant(result)

            if result.canConvert(QtCore.QVariant.Int):
                return int(result.toInt()[0])
            else:
                return None

    def leaveEmptyOnNone(self, txl, thisText):
        #thisName = txl.objectName()
        if thisText:
            txl.setText(thisText)
        else:
            txl.setText(QtCore.QString())

    def manageAustrittsdatum(self, austrittsdatum = None):
        if not austrittsdatum:
            austrittsdatum = QtCore.QDate(2099, 12, 31)
        else:
            austrittsdatum = QtCore.QDate(austrittsdatum)

        self.ui.dateAustrittsDatum.setDate(austrittsdatum)

        if austrittsdatum.year() == 2099:
            self.ui.cbxAustrittsgrund.setVisible(False)
            self.ui.lblAustrittsgrund.setVisible(False)
            self.ui.btnAustrittHeute.setVisible(True)
        else:
            self.ui.cbxAustrittsgrund.setVisible(True)
            self.ui.lblAustrittsgrund.setVisible(True)
            self.ui.btnAustrittHeute.setVisible(False)
            self.cbxValueFromString(self.ui.cbxAustrittsgrund, \
                                    self.mitglied.austrittsgrund.austrittsgrund)

    def setMemberValues(self):
        '''setzt die Eingabefelder auf die Werte von memberValues'''

        if self.memberId <= 0: #neues Mitglied
            # default values

            self.ui.dateEintrittsDatum.setDate(QtCore.QDate.currentDate())
            self.manageAustrittsdatum(QtCore.QDate(2099, 12, 31))
            self.ui.radNatuerlichePerson.setVisible(True) # falls Reset gedrückt wird
            self.ui.radJuristischePerson.setVisible(True)
            self.mitglied = None
            self.isNaturalMember = True
            self.ui.radNatuerlichePerson.setChecked(True)
            self.legalMember.hide()
            self.ui.dateEinzugsermaechtigung.setDate(QtCore.QDate())
        else:
            # feststellen ob natürliches oder juristisches Mitglied
            self.isNaturalMember = True
            mitglieder = datamodel.MitgliedNatuerlich.query.filter_by(\
                                    mitgliedsnummer=self.memberId).all()

            if len(mitglieder) == 0:
                self.isNaturalMember = False
                mitglieder = datamodel.MitgliedJuristisch.query.filter_by(\
                                    mitgliedsnummer=self.memberId).all()

            if len(mitglieder) == 0:
                QtGui.QMessageBox.error(None, "", "Mitglied nicht gefunden")
                return None
            else:
                self.mitglied = mitglieder[0]

            #Daten aus DB einlesen
            if self.isNaturalMember:
                self.ui.radNatuerlichePerson.click()
                self.naturalMember.ui.txlName.setText(self.mitglied.mitgliedsname)
                self.cbxValueFromString(self.naturalMember.ui.cbxAnrede, \
                                        self.mitglied.anrede.anrede)
                self.leaveEmptyOnNone(self.naturalMember.ui.txlTitel, self.mitglied.titel)
                self.naturalMember.ui.txlVorname.setText(self.mitglied.vorname)
                self.leaveEmptyOnNone(self.naturalMember.ui.txlNamenszusatz, \
                                          self.mitglied.namenszusatz)
                self.naturalMember.ui.dateGeburtsdatum.setDate(self.mitglied.geburtsdatum)
                self.leaveEmptyOnNone(self.naturalMember.ui.txlBeruf, \
                                      self.mitglied.beruf)
                if self.mitglied.hauptmitglied:
                    hauptMitglied = self.mitglied.hauptmitglied.mitgliedsname
                else:
                    hauptMitglied = QtCore.QString()

                self.naturalMember.ui.txlHauptmitglied.setText(hauptMitglied)
                self.naturalMember.ui.txtHinweise.setPlainText(self.mitglied.hinweise)
            else:
                self.ui.radJuristischePerson.click()
                self.legalMember.ui.txlName.setText(self.mitglied.mitgliedsname)
                self.legalMember.ui.txlAnsprechpartner.setText(self.mitglied.ansprechpartner)
                self.legalMember.ui.txtHinweise.setPlainText(self.mitglied.hinweise)

            self.ui.txlStrasse.setText(self.mitglied.strasse)
            self.ui.txlHnr.setText(str(self.mitglied.hnr))
            self.leaveEmptyOnNone(self.ui.txlHnrZusatz, self.mitglied.hnrzusatz)
            self.leaveEmptyOnNone(self.ui.txlAdresszusatz, self.mitglied.adresszusatz)
            self.cbxValueFromString(self.ui.cbxOrt, \
                                    self.mitglied.ort.plz + " " + self.mitglied.ort.ort)
            self.ui.txlMitgliedsnummer.setText(str(self.mitglied.mitgliedsnummer))
            self.cbxValueFromString(self.ui.cbxKategorie, \
                                    self.mitglied.mitgliedsgruppe.mitgliedsgruppe)
            self.cbxValueFromString(self.ui.cbxBeitragsgruppe, \
                                    self.mitglied.beitragsgruppe.beitragsgruppe)
            self.leaveEmptyOnNone(self.ui.txlIndividuellerBeitrag, \
                                  self.intToString(self.mitglied.individueller_beitrag))
            self.cbxValueFromString(self.ui.cbxZahlungsart, \
                                    self.mitglied.zahlungsart.zahlungsart)
            self.cbxValueFromString(self.ui.cbxZahlweise, \
                                    self.mitglied.zahlweise.zahlweise)
            eintrittsdatum = self.ui.dateEintrittsDatum.setDate(self.mitglied.eintrittsdatum)
            self.manageAustrittsdatum(self.mitglied.austrittsdatum)
            self.leaveEmptyOnNone(self.ui.txlKontonummer, self.intToString(self.mitglied.kontonummer))
            self.leaveEmptyOnNone(self.ui.txlKontoInhaber, self.mitglied.kontoinhaber)
            self.leaveEmptyOnNone(self.ui.txlIban, self.mitglied.iban)
            self.leaveEmptyOnNone(self.ui.txlBic, self.mitglied.bic)
            bank = self.mitglied.bank

            if bank:
                blz = self.intToString(bank.blz)
                institut = bank.bank
            else:
                blz = QtCore.QString()
                institut = QtCore.QString()

            self.ui.txlBlz.setText(blz)
            self.ui.txlInstitut.setText(institut)

            if self.mitglied.einzugsermaechtigungsdatum:
                self.ui.dateEinzugsermaechtigung.setDate(self.mitglied.einzugsermaechtigungsdatum)
            else:
               self.ui.dateEinzugsermaechtigung.setDate(QtCore.QDate())

        self.ui.radOrtCbx.toggle()
        self.fillEmail()
        self.fillTelefon()
        self.fillZahlungen()
        self.fillSchreiben()

    def saveToDb(self):
        # Werte festlegen

        if self.isNaturalMember:
            thisAnrede = unicode(self.naturalMember.ui.cbxAnrede.currentText())
            anrede = datamodel.Anrede.get_by(anrede = thisAnrede)
            titel = self.nonify(self.naturalMember.ui.txlTitel)
            vorname = self.nonify(self.naturalMember.ui.txlVorname)
            mitgliedsname = self.nonify(self.naturalMember.ui.txlName)
            namenszusatz = self.nonify(self.naturalMember.ui.txlNamenszusatz)
            beruf = self.nonify(self.naturalMember.ui.txlBeruf)
            geburtsdatum = self.qDateToDate(self.naturalMember.ui.dateGeburtsdatum.date())
            hauptmitglied = None
            hauptmitgliedsnummer = self.nonifyInt(self.naturalMember.ui.txlHauptmitglied)

            if hauptmitgliedsnummer:
                hauptmitglied = datamodel.MitgliedNatuerlich.get_by(\
                    mitgliedsnummer=hauptmitgliedsnummer)

            hinweise = self.naturalMember.ui.txtHinweise.toPlainText()
            hinweise = unicode(hinweise)
        else:
            mitgliedsname = self.nonify(self.legalMember.ui.txlName)
            ansprechpartner = self.nonify(self.legalMember.ui.txlAnsprechpartner)
            hauptmitglied = None
            hinweise = str(self.legalMember.ui.txtHinweise.toPlainText())

        if not hauptmitglied:
            #gemeinsame Adresse und Zahlung
            strasse = self.nonify(self.ui.txlStrasse)
            hnr = self.nonifyInt(self.ui.txlHnr)
            hnrzusatz = self.nonify(self.ui.txlHnrZusatz)
            adresszusatz = self.nonify(self.ui.txlAdresszusatz)

            if self.ui.radOrtCbx.isChecked():
                thisPlzOrt = unicode(self.ui.cbxOrt.currentText()).split()
                thisPlz = thisPlzOrt[0]
                thisOrt = None

                for i in range(1, len(thisPlzOrt)):
                    if thisOrt:
                        thisOrt = thisOrt + " " + thisPlzOrt[i]
                    else:
                        thisOrt = thisPlzOrt[i]
            else:
                thisPlz = self.nonify(self.ui.txlPlz)
                thisOrt = self.nonify(self.ui.txlOrt)

            newOrt = True

            for einOrt in datamodel.Ort.query.filter_by(plz=thisPlz).all():
                if einOrt.ort == thisOrt:
                    ort = einOrt
                    newOrt = False
                    break

            if newOrt:
                thisLand = unicode(self.ui.cbxLand.currentText())
                land = datamodel.Land.get_by(land = thisLand)

                ort = datamodel.Ort(plz = thisPlz, ort = thisOrt)
                ort.land = land

            thisZahlungsart = unicode(self.ui.cbxZahlungsart.currentText())
            zahlungsart = datamodel.Zahlungsart.get_by(zahlungsart=thisZahlungsart)
            thisZahlweise = unicode(self.ui.cbxZahlweise.currentText())
            zahlweise = datamodel.Zahlweise.get_by(zahlweise = thisZahlweise)

            #Bankverbindung
            kontonummer = self.nonifyInt(self.ui.txlKontonummer)
            kontoinhaber = self.nonify(self.ui.txlKontoInhaber)
            blz = self.nonifyInt(self.ui.txlBlz)

            if blz:
                banken = datamodel.Bank.query.filter_by(blz=blz).all()

                if len(banken) > 0:
                    bank = banken[0]
                else: #Bank neu aufnehmen
                    bank = datamodel.Bank(blz=blz, bank = self.nonify(self.ui.txlInstitut))
            else:
                bank = None

            iban = self.nonify(self.ui.txlIban)
            bic = self.nonify(self.ui.txlBic)
            einzugsermaechtigungsDatum = self.ui.dateEinzugsermaechtigung.date()

            if einzugsermaechtigungsDatum == QtCore.QDate():
                einzugsermaechtigungsDatum = None
            else:
                einzugsermaechtigungsDatum = self.qDateToDate(einzugsermaechtigungsDatum)

        #Mitgliedschaft
        thisMitgliedsgruppe = unicode(self.ui.cbxKategorie.currentText())
        mitgliedsgruppe = datamodel.Mitgliedsgruppe.get_by(mitgliedsgruppe = thisMitgliedsgruppe)
        thisBeitragsgruppe = unicode(self.ui.cbxBeitragsgruppe.currentText())
        beitragsgruppe = datamodel.Beitragsgruppe.get_by(beitragsgruppe = thisBeitragsgruppe)
        individuellerBeitrag = self.nonifyInt(self.ui.txlIndividuellerBeitrag)
        eintrittsdatum = self.qDateToDate(self.ui.dateEintrittsDatum.date())
        austrittsdatum = self.ui.dateAustrittsDatum.date()

        if austrittsdatum.isNull():
            austrittsgrund = None
        else:

            if austrittsdatum.year() == 2099:
                austrittsdatum = None
                austrittsgrund = None
            else:
                austrittsdatum = self.qDateToDate(austrittsdatum)
                thisAustrittsgrund = unicode(self.ui.cbxAustrittsgrund.currentText())
                austrittsgrund = datamodel.Austrittsgrund.get_by(austrittsgrund = thisAustrittsgrund)

        # Werte eintragen
        if self.isNaturalMember:
            if self.memberId < 0:
                self.mitglied = datamodel.MitgliedNatuerlich()

            self.mitglied.anrede = anrede
            self.mitglied.titel = titel
            self.mitglied.vorname = vorname
            self.mitglied.namenszusatz = namenszusatz
            self.mitglied.geburtsdatum = geburtsdatum
            self.mitglied.beruf = beruf
            self.mitglied.hauptmitglied = hauptmitglied
        else:
            if self.memberId < 0:
                self.mitglied = datamodel.MitgliedJuristisch()

            self.mitglied.ansprechpartner = ansprechpartner

        self.mitglied.mitgliedsname = mitgliedsname
        self.mitglied.hinweise = hinweise

        if not hauptmitglied:
            self.mitglied.strasse = strasse
            self.mitglied.hnr = hnr
            self.mitglied.hnrzusatz = hnrzusatz
            self.mitglied.adresszusatz = adresszusatz
            self.mitglied.ort = ort
            self.mitglied.zahlungsart = zahlungsart
            self.mitglied.zahlweise = zahlweise
            self.mitglied.kontonummer = kontonummer
            self.mitglied.kontoinhaber = kontoinhaber
            self.mitglied.bank = bank
            self.mitglied.iban = iban
            self.mitglied.bic = bic
            self.mitglied.einzugsermaechtigungsdatum = einzugsermaechtigungsDatum

        self.mitglied.mitgliedsgruppe = mitgliedsgruppe
        self.mitglied.beitragsgruppe = beitragsgruppe
        self.mitglied.individueller_beitrag = individuellerBeitrag
        self.mitglied.eintrittsdatum = eintrittsdatum
        self.mitglied.austrittsdatum = austrittsdatum
        self.mitglied.austrittsgrund = austrittsgrund
        self.mitglied.letzte_aenderung = datetime.now()

        for tbl in [self.ui.tblEmail, self.ui.tblTelefon, self.ui.tblZahlungen]:
            model = tbl.model()

            for i in range(model.rowCount()):
                #self.ui.tblEmail.doubleClicked(model.index(i,  3))
                rec = model.record(i)
                test = rec.value(1).toInt()[0]

                if test <= 0:
                    rec.setValue(1, self.mitglied.mitgliedsnummer)
                    test = rec.value(3).toString()
                    model.setRecord(i, rec)

            if model.submitAll():

                if tbl == self.ui.tblZahlungen:
                    self.newZahlungRows = -1
            else:
                self.showSubmitAllError(model)
                self.changed()
                elixir.session.rollback()
                return False

        elixir.session.commit()
        return True


    def showQueryError(self, query):
        QtGui.QMessageBox.warning(None, "Database Error", \
            QtCore.QString("%1 \n %2").arg(query.lastError().text()).arg(query.lastQuery()))

    def showSubmitAllError(self, model):
        QtGui.QMessageBox.warning(None, "Database Error", \
            QtCore.QString("%1").arg(model.lastError().text()))

class NaturalMember(QtGui.QWidget):
    def __init__(self, parentWidget = 0, memberId = -9999):
        QtGui.QWidget.__init__(self, parentWidget)

        self.ui = Ui_MitgliedNatuerlich()
        self.ui.setupUi(self)
        self.memberId = memberId

class LegalMember(QtGui.QWidget):
    def __init__(self, parentWidget = 0, memberId = -9999):
        QtGui.QWidget.__init__(self, parentWidget)

        self.ui = Ui_MitgliedJuristisch()
        self.ui.setupUi(self)
        self.memberId = memberId

