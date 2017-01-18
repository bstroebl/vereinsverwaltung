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

import subprocess
import os
import sys
import tempfile
import numberToWord
from PyQt4 import QtCore, QtGui, QtSql, QtXml
from datetime import datetime
from Ui_MainWindow import Ui_MainWindow
from dialogs import LookupTableDialog, LookupTableRelationDialog, VerbindungsDialog, \
    SchreibenDialog, SMTPDialog
import resources_rc
import datamodel
import elixir
import smtplib
#for guessing MIME type based on file extensions
import mimetypes
from email import MIMEText, Header, MIMEMultipart, MIMEAudio, MIMEBase, MIMEImage, encoders
#from sqlalchemy import select
from member import MemberData

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QtCore.QCoreApplication.setOrganizationName("Verein")
        QtCore.QCoreApplication.setApplicationName("Mitgliederverwaltung")

        self.ui.actNeu.setShortcut(QtGui.QKeySequence("Ctrl+N"))
        self.ui.actOpen.setShortcut(QtGui.QKeySequence("Ctrl+O"))

        self.ui.tabMitglied.removeTab(0) #soll leer sein
        self.newMemberId = 0
        self.smtpPassword = None
        #currentMember = MemberData(self.ui.tabMitglied.currentWidget())

        #Datenbank
        self.db = None
        self.dbfile = None
        self.connectDb()
        self.initDataFromDB()

    def __debug(self, msg):
        QtGui.QMessageBox.information(self, "Debug", msg)

    def initDataFromDB(self):
        if self.db:
            self.prepareCbxValues()
            self.setupMemberModel()
            self.fillMemberTable()

    def setupMemberModel(self):

         if self.db:
            self.memberModel = QtSql.QSqlTableModel()
            self.memberModel.setTable("mitglied")
            self.memberModel.setHeaderData(0, QtCore.Qt.Horizontal, u"Nr.")
            self.memberModel.setHeaderData(1, QtCore.Qt.Horizontal, u"Name")
            self.memberModel.setHeaderData(2, QtCore.Qt.Horizontal, u"Vorname")
            self.ui.tblMitglieder.setModel(self.memberModel)

            for i in range(3, 50):
                self.ui.tblMitglieder.setColumnHidden(i, True)

    def prepareCbxValues(self):
        if self.db:
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

            listWidget = self.ui.lstKriteriumUnd
            listWidget.clear()

            for kriterium in datamodel.Suchkriterium.query.order_by(\
                   datamodel.Suchkriterium.suchkriterium).all():
                parentItem = QtGui.QListWidgetItem(QtCore.QString(kriterium.suchkriterium))
                parentItem.setCheckState(False)
                listWidget.addItem(parentItem)
            #QtGui.QMessageBox.information(None,"XML",self.enumDoc.toString())

    def noDbConnection(self):
        QtGui.QMessageBox.warning(self, "Datenbank-Fehler",
                u"Keine Verbindung zur Datenbank!")

    def getDBSettings(self):
        settings = QtCore.QSettings() #u"Verein", u"Mitgliederverwaltung")
        settings.beginGroup(u"DB_Connection")

        if len(settings.childKeys()) > 0:
            self.dbfile = str(settings.value("dbfile").toString())
            settings.endGroup()
            return True
        else:
            settings.endGroup()
            return None

    def getSMTPSettings(self):
        settings = QtCore.QSettings() #u"Verein", u"Mitgliederverwaltung")
        settings.beginGroup(u"SMTP_Connection")
        host = str(settings.value("host", "").toString())
        port = str(settings.value("port", "").toString())
        user = str(settings.value("user", "").toString())
        password = str(settings.value("password", "").toString())
        ssl = settings.value("ssl", "False").toString()
        ssl = (ssl == "True")
        sender = str(settings.value("sender", "").toString())
        sendername = str(settings.value("sendername", "").toString())
        settings.endGroup()

        return [host, port, user, password, sender, ssl, sendername]

    def setDBSettings(self):
        if self.dbfile != None:
            settings = QtCore.QSettings() #u"Verein", u"Mitgliederverwaltung")
            settings.beginGroup(u"DB_Connection")
            settings.setValue("dbfile", self.dbfile)
            settings.endGroup()

    def setSMTPSettings(self):
        dlg = SMTPDialog(self.getSMTPSettings())
        return dlg.exec_()

    def setSMTPPassword(self, host):
        '''returns boolean if password was set'''
        msg = u"Passwort für den Mailserver " + host + " eingeben"
        password, ok = QtGui.QInputDialog.getText(None, "Passwort",
                 msg, QtGui.QLineEdit.Password)

        if ok:
            self.smtpPassword = password
        return ok

    def getPathSettings(self):
        settings = QtCore.QSettings() #u"Verein", u"Mitgliederverwaltung")
        settings.beginGroup(u"documentpath")

        if len(settings.childKeys()) > 0:
            speicherpfad = settings.value("speicherpfad").toString()
            settings.endGroup()
            return speicherpfad
        else:
            settings.endGroup()
            return None

    def setTitle(self):
        self.setWindowTitle("Mitgliederverwaltung - " + self.dbfile)

    def initDb(self, dbfile):
        '''benutze übergebene Sqite-Db'''
        self.dbfile = str(dbfile)
        self.setTitle()
        self.setDBSettings()
        #alle offenen Tabs schliessen
        self.closeAllTabs()
        elixir.session.close()
        # mit neuer DB verbinden
        self.connectDb()
        self.initDataFromDB()

    def connectDb(self):
        '''Verbindung mit DB aufbauen'''
        if self.dbfile == None:
            mySettings = self.getDBSettings()

            if not mySettings:
                self.on_actOpen_triggered()

        if self.dbfile != None:
            self.setTitle()
            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(self.dbfile)
            ok = db.open()

            if ok:
                self.db = db
                elixir.metadata.bind = "sqlite:///" + self.dbfile
                elixir.metadata.bind.echo = True
                elixir.setup_all(True) # Verbindung aufbauen und Tabellen anlegen
                # bleibt so, damit bei einer DB-Neuanlage aber gespeicherter
                # Verbindung die Tabellen angelegt werden, ist unschädlich, wenn
                # es die Tabellen schon gibt
            else:
                self.noDbConnection()
                self.db = None

    def memberTableSql(self):
        '''gibt die SQL zurück, mit der die Mitgliedertabelle gefüllt wird'''

        return ["SELECT m.id, COLAESCE(mn.vorname, '') || m.mitgliedsname FROM mitglied m " +
                "LEFT JOIN mitglied_natuerlich mn ON m.id = mn.mitglied_id)",
                "ORDER BY mitgliedsname"]

    def fillMemberTable(self):
        if not self.db:
            self.noDbConnection()
        else:
            self.memberModel.select()
            ss = self.memberModel.selectStatement()

            for i in range(1):
                self.ui.tblMitglieder.resizeColumnToContents(i)

    def showQueryError(self, query):
        QtGui.QMessageBox.warning(None, "Database Error", \
            QtCore.QString("%1 \n %2").arg(query.lastError().text()).arg(query.lastQuery()))

    def showLookupTableDialog(self, tableName, headers, \
        successfullySavedMsg = u"Änderungen werden nur bei neu geöffneten Mitgliedsformularen sichtbar!"):
        '''creates a QDialog with a QTableView that shows tableName'''

        dlg = LookupTableDialog(tableName, headers, self.db, successfullySavedMsg, None, self)
        dlg.show()
        result = dlg.exec_()

        if result == 1:
            self.prepareCbxValues()

    def closeAllTabs(self):
        while(self.ui.tabMitglied.currentIndex() > -1):
            memberData = self.ui.tabMitglied.currentWidget()

            if memberData.childrenRect().height() > 0:
                memberData = memberData.childAt(1, 1)
                memberData.closeBtn.click()

    def closeEvent(self, event):
        self.closeAllTabs()

        if self.db:
            self.db.close()
            elixir.session.rollback()
            elixir.session.close()

    def sendEmail(self, thisSchreiben, showErrors = True):
        '''returns true on success'''

        #Verbindungsdaten
        while True:
            smtpSettings = self.getSMTPSettings()
            host = smtpSettings[0]
            port = smtpSettings[1]
            user = smtpSettings[2]
            password = smtpSettings[3]
            sender = smtpSettings[4]
            ssl = smtpSettings[5]
            sendername = smtpSettings[6]

            if host == "" or sender == "":
                if self.setSMTPSettings() == 0:
                    return None
            else:
                break

        if port == "":
            port = None
        else:
            port = int(port)

        # wurde seit das Programm läuft bereits das Passwort eingegeben?
        if not self.smtpPassword:
            if password == "" and user != "": # password in settings nicht gespeichert
                ok = self.setSMTPPassword(host)

                if not ok:
                    return False
            else:
                self.smtpPassword = password

        #haben alle Mitglieder eine gültige Emailadresse?
        keineEmailAdresse = []
        fehlerInEmailAdressen = []
        valideEmailAdressen = []

        for mitglied in thisSchreiben.mitglieder:
            emailAdressen = mitglied.emailadressen

            if len(emailAdressen) == 0:
                keineEmailAdresse.append(mitglied)
            else:
                valideAdresse = None

                for emailAdresse in emailAdressen:
                    if len(emailAdresse.fehler) == 0:
                        valideAdresse = emailAdresse.emailadresse
                        break

                if valideAdresse:
                    valideEmailAdressen.append(valideAdresse)
                else:
                    fehlerInEmailAdressen.append(mitglied)

        msgKeine = None

        for mitglied in keineEmailAdresse:
            thisSchreiben.mitglieder.remove(mitglied)

            if not msgKeine:
                msgKeine = u"folgende Mitglieder haben keine Email-Adresse: \n"

            msgKeine = msgKeine + u"Mitglnr " + str(mitglied.mitgliedsnummer) + \
                ": " + str(mitglied.mitgliedsname) + "\n"

        msgFehler = None

        if len(fehlerInEmailAdressen) > 0:

            for mitglied in fehlerInEmailAdressen:

                if not msgFehler:
                    msgFehler = u"folgende Mitglieder haben keine fehlerfreie Email-Adresse: \n"

                msgFehler = msgFehler + u"Mitglnr " + str(mitglied.mitgliedsnummer) + \
                    ": " + str(mitglied.mitgliedsname) + "\n"

            reply = QtGui.QMessageBox.question(self, u"Fehlerhafte Adressen",
                msgFehler + u"\n Soll trotzdem versucht werden, " + \
                    "die Nachricht an diese Mitglieder zu versenden?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:

                for mitglied in fehlerInEmailAdressen:
                    valideEmailAdressen.append(mitglied.emailadressen[0].emailadresse)
                    msgFehler = None

            elif reply == QtGui.QMessageBox.No:

                for mitglied in fehlerInEmailAdressen:
                    thisSchreiben.mitglieder.remove(mitglied)

        if len(valideEmailAdressen) == 0:
            if showErrors:
                QtGui.QMessageBox.critical(None, u"Fehler beim Senden der Mail",
                    u"Kein Empfänger hat eine gültige Email-Adresse!")
            return False

        #Mail abschicken
        if ssl:
            smtp = smtplib.SMTP_SSL()
        else:
            smtp = smtplib.SMTP()

        try:
            if port:
                smtp.connect(host, port)
            else:
                smtp.connect(host)

        except:
            if showErrors:
                QtGui.QMessageBox.critical(None, u"Verbindungsfehler", \
                    u"Keine Verbindung mit dem SMTP-Server " + host + \
                    u" möglich!")
            return False

        if user != "":
            while True:
                try:
                    smtp.login(user, self.smtpPassword)
                    break
                except smtplib.SMTPAuthenticationError:
                    msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                        u"Verbindungsfehler", u"Kein Login auf dem SMTP-Server " + \
                        host + u" möglich!")
                    msgBox.addButton(u"Passwort ändern", QtGui.QMessageBox.AcceptRole)
                    msgBox.addButton("Abbrechen", QtGui.QMessageBox.RejectRole)

                    if msgBox.exec_() == QtGui.QMessageBox.AcceptRole:
                        self.setSMTPPassword(host)
                    else:
                        smtp.quit()
                        return False


        # Schicken der Mail
        #Quelle des folgenden: http://docs.python.org/library/email-examples.html
        if sendername != "":
            sender = sendername + " <" + sender + ">"

        outer = MIMEMultipart.MIMEMultipart()
        outer['Subject'] = thisSchreiben.titel
        outer['From'] = sender

        if len(valideEmailAdressen) == 1:
            outer['To'] = ', '.join(valideEmailAdressen)
        else:
            outer['To'] = sender #Eine To-Adresse für BCC

        mailMsg = MIMEText.MIMEText(thisSchreiben.text.encode('utf-8'), _charset='utf-8')
        outer.attach(mailMsg)

        for anhang in thisSchreiben.anhaenge:
            path = anhang.pfad
            ctype, encoding = mimetypes.guess_type(path)

            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                fp = open(path)
                # Note: we should handle calculating the charset
                msg = MIMEText.MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'image':
                fp = open(path, 'rb')
                msg = MIMEImage.MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(path, 'rb')
                msg = MIMEAudio.MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(path, 'rb')
                msg = MIMEBase.MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
                fp.close()
                # Encode the payload using Base64
                encoders.encode_base64(msg)
            # Set the filename parameter
            msg.add_header('Content-Disposition', 'attachment',
                           filename = os.path.basename(path))
            outer.attach(msg)

        composed = outer.as_string()
        fp = open("/tmp/test.mail", 'w')
        fp.write(composed)
        fp.close()

        msgSmtp = ""

        try:
            #zweites Argument von sendmail ist die Liste der Adressaten, dies ist völlig unabhängig vom To in der MIME-message
            adressErrors = smtp.sendmail(sender, valideEmailAdressen, composed)
        except smtplib.SMTPRecipientsRefused as e:
            addressErrors = e.recipients
        except smtplib.SMTPSenderRefused:
            msgSmtp = u"Sender " + sender + u" von SMTP-Server nicht akzepiert!"
        except smtplib.SMTPDataError:
            msgSmtp = u"SMTP-Server weist die Daten zurück!"
        # ungültige Absenderadressen werden vom empfangenden Mailserver an die
        # Absenderadresse geschickt und landen dort im Posteingang, d.h.
        # 1) fehlerhafte Emailadressen können hier nicht als solche markiert werden
        # 2) Dem Mitglied wird das Schreiben zugeordnet, obwohl er es garnicht
        #    empfangen hat.

        smtp.quit()

        if msgSmtp != "":
            QtGui.QMessageBox.critical(None, u"Fehler beim Senden der Email", errMsg)
            return False
        else:

            if showErrors:
                if msgKeine or msgFehler:
                    errMsg = u"Diese Mitglieder haben die Email nicht erhalten:"

                    if msgKeine:
                        errMsg = errMsg + "\n" + msgKeine
                    if msgFehler:
                        errMsg = errMsg + "\n" + msgFehler

                    QtGui.QMessageBox.critical(None, u"Fehler beim Senden der Email", errMsg)

            return True

    def printLetter(self, thisSchreiben):
        '''returns true on success'''
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            doc = QtGui.QTextDocument()
            doc.setHtml(QtCore.QString(thisSchreiben.text))
            doc.print_(dialog.printer())
            return True
        else:
            return False

    def makeSchreiben(self,  newSchreiben,  forEdit = True,  parent = None,  noEmail = False):
        dlg = SchreibenDialog(newSchreiben, forEdit,  parent,  noEmail)
        dlg.showMaximized()
        result = dlg.exec_()

        if result == 1:

            if newSchreiben.art.schreibenart == "Email":
                sent = self.sendEmail(newSchreiben)

                if sent:
                    QtGui.QMessageBox.information(None, "",  u"Email gesendet!")
            else:
                sent = self.printLetter(newSchreiben)

            if sent:
                elixir.session.commit()
            else:
                elixir.session.rollback()

        else:
            elixir.session.rollback()

    def isNaturalMember(self,  memberId):
        mitglied = datamodel.MitgliedNatuerlich.get_by(\
                                    mitgliedsnummer=memberId)

        return (mitglied != None)

    #SLOTS
    # Mitgliedssuche und -anzeige
    @QtCore.pyqtSlot(QtGui.QListWidgetItem, name="on_lstKriteriumUnd_itemClicked")
    def on_lstKriteriumUnd_itemClicked(self, thisItem):
        self.ui.btnFindeMitglied.click()

    @QtCore.pyqtSlot(name="on_btnFindeMitglied_clicked")
    def on_btnFindeMitglied_clicked(self):
        #QtGui.QMessageBox.information(None,"","on_btnFindeMitglied_clicked")
        searchString = self.ui.txlFindeMitglied.text()
        sqlString = QtCore.QString()

        if not searchString.isEmpty():
            sqlString.append("(")
            ok = searchString.toInt()[1]

            if ok:
                sqlString.append("id = ").append(searchString)
            else:
                searchString.replace("*", "%")
                sqlString.append("lower(mitgliedsname) LIKE \'")
                sqlString.append(searchString.toLower())
                sqlString.append("\'")

        listWidget = self.ui.lstKriteriumUnd

        for i in range(listWidget.count()):
            item = listWidget.item(i)

            if item.checkState() == 2:

                if sqlString.isEmpty():
                    sqlString.append("(")
                else:
                    sqlString.append(") AND (")

                suchkriterium = datamodel.Suchkriterium.query.filter_by(\
                    suchkriterium = unicode(item.text())).first()
                sqlString.append(suchkriterium.abfrage)

        if self.db:

            if sqlString.isEmpty():
                pass
                #QtGui.QMessageBox.information(None,"Mitgliedssuche",
                #            u"keine Suchkriterien eingegeben")
            else:
                sqlString.append(")")

            self.memberModel.setFilter(sqlString)
            self.fillMemberTable()

    @QtCore.pyqtSlot(name="on_txlFindeMitglied_returnPressed")
    def on_txlFindeMitglied_returnPressed(self):
        self.ui.btnFindeMitglied.click()

    @QtCore.pyqtSlot(int, name="on_chkNurHaupt_stateChanged")
    def on_chkNurHaupt_stateChanged(self, checkState):
        self.ui.btnFindeMitglied.click()

    @QtCore.pyqtSlot(int, name="on_chkNurAktiv_stateChanged")
    def on_chkNurAktiv_stateChanged(self, checkState):
        self.ui.btnFindeMitglied.click()

    @QtCore.pyqtSlot(QtCore.QModelIndex, name="on_tblMitglieder_doubleClicked")
    def on_tblMitglieder_doubleClicked(self, thisModelIndex):
        mitgliedsnummer = thisModelIndex.sibling(thisModelIndex.row(), 0).data().toString()
        mitgliedsname = thisModelIndex.sibling(thisModelIndex.row(), 1).data().toString()
        vorname = thisModelIndex.sibling(thisModelIndex.row(), 2).data().toString()

        if vorname.isEmpty():
            displayname = mitgliedsname
        else:
            displayname = vorname + " " + mitgliedsname

        makeNew = True

        # werden die Daten dieses Mitglieds bereits angezeigt?
        for i in range(self.ui.tabMitglied.count()):
            tab = self.ui.tabMitglied.widget(i)

            if tab.objectName() == mitgliedsnummer:
                makeNew = False
                self.ui.tabMitglied.setCurrentIndex(i)
                break

        if makeNew:
            newTab = QtGui.QWidget()
            newTab.setObjectName(mitgliedsnummer)
            MemberData(self.db, self, \
                       newTab, int(mitgliedsnummer))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/identity_ok.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.tabMitglied.addTab(newTab, icon, displayname)
            self.ui.tabMitglied.setCurrentWidget(newTab)

    # menus
    @QtCore.pyqtSlot()
    def on_actAnrede_triggered(self):
        self.showLookupTableDialog("anrede", [None, "Anrede"])

    @QtCore.pyqtSlot()
    def on_actOrt_triggered(self):
        dlg = LookupTableRelationDialog("ort", \
            [None, "Ort", "PLZ", "Land"], \
            self.db, \
            [3, "land", "id", "land"], \
            u"Änderungen werden nur bei neu geöffneten Mitgliedsformularen sichtbar!", \
            None, self)
        dlg.show()
        result = dlg.exec_()

        if result == 1:
            self.prepareCbxValues()

    @QtCore.pyqtSlot()
    def on_actLand_triggered(self):
        self.showLookupTableDialog("land", [None, "Land", u"Länderkürzel"])

    @QtCore.pyqtSlot()
    def on_actBeitragsgruppe_triggered(self):
        self.showLookupTableDialog("beitragsgruppe", [None, "Beitragsgruppe", "Jahresbeitrag"])

    @QtCore.pyqtSlot()
    def on_actErweiterteSuche_triggered(self):
        self.showLookupTableDialog("suchkriterium", [None, "Kriterium", "SQL-String"], "")

    @QtCore.pyqtSlot()
    def on_actMitgliedsgruppe_triggered(self):
        self.showLookupTableDialog("mitgliedsgruppe", [None, "Mitgliedsgruppe"])

    @QtCore.pyqtSlot()
    def on_actAustrittsgrund_triggered(self):
        self.showLookupTableDialog("austrittsgrund", [None, "Austrittsgrund"])

    @QtCore.pyqtSlot()
    def on_actZahlungsart_triggered(self):
        self.showLookupTableDialog("zahlungsart", [None, "Zahlungsart"])

    @QtCore.pyqtSlot()
    def on_actZahlweise_triggered(self):
        self.showLookupTableDialog("zahlweise", [None, "Zahlweise"])

    @QtCore.pyqtSlot()
    def on_actHinweisEMail_triggered(self):
        self.showLookupTableDialog("hinweis_email", [None, "Hinweis"])

    @QtCore.pyqtSlot()
    def on_actHinweisTelFax_triggered(self):
        self.showLookupTableDialog("hinweis_telefonfax", [None, "Hinweis"])

    @QtCore.pyqtSlot()
    def on_actBank_triggered(self):
        self.showLookupTableDialog("bank", ["BLZ", "Bank"])

    @QtCore.pyqtSlot()
    def on_actHinweisZahlung_triggered(self):
        self.showLookupTableDialog("hinweis_zahlung", [None, "Hinweis"])

    @QtCore.pyqtSlot()
    def on_actArt_triggered(self):
        self.showLookupTableDialog("schreibenart", [None, "Art des Schreibens"])

    @QtCore.pyqtSlot()
    def on_actInitialize_triggered(self):
        elixir.create_all() # Tabellen anlegen

        # einige Werte anlegen, falls die DB leer ist

        if len(datamodel.Anrede.query.all()) == 0:
            datamodel.Anrede(anrede = u'Herr')
            datamodel.Anrede(anrede = u'Frau')

        if len(datamodel.Austrittsgrund.query.all()) == 0:
            datamodel.Austrittsgrund(austrittsgrund = u'Kündigung')
            datamodel.Austrittsgrund(austrittsgrund = u'Ausschluss')

        if len(datamodel.HinweisEmail.query.all()) == 0:
            datamodel.HinweisEmail(hinweis = u'privat')
            datamodel.HinweisEmail(hinweis = u'dienstlich')

        if len(datamodel.HinweisTelefonFax.query.all()) == 0:
            datamodel.HinweisTelefonFax(hinweis = u'Tel. privat')
            datamodel.HinweisTelefonFax(hinweis = u'Tel. dienstlich')
            datamodel.HinweisTelefonFax(hinweis = u'mobil')
            datamodel.HinweisTelefonFax(hinweis = u'Fax dienstlich')
            datamodel.HinweisTelefonFax(hinweis = u'Fax privat')

        if len(datamodel.Land.query.all()) == 0:
            datamodel.Land(land = u'Deutschland', kuerzel = "D")

        if len(datamodel.Zahlungsart.query.all()) == 0:
            datamodel.Zahlungsart(zahlungsart = u'Überweisung')
            datamodel.Zahlungsart(zahlungsart = u'Bankeinzug')

        if len(datamodel.Zahlweise.query.all()) == 0:
            datamodel.Zahlweise(zahlweise = u'jährlich')

        if len(datamodel.Schreibenart.query.all()) == 0:
            datamodel.Schreibenart(schreibenart = u'Email')
            datamodel.Schreibenart(schreibenart = u'Brief')
            #datamodel.Schreibenart(schreibenart = 'Fax')

        if len(datamodel.Mitgliedsgruppe.query.all()) == 0:
            datamodel.Mitgliedsgruppe(mitgliedsgruppe = u'Mitglied')
            datamodel.Mitgliedsgruppe(mitgliedsgruppe = u'Spender')

        if len(datamodel.Beitragsgruppe.query.all()) == 0:
            newBeitragsgruppe = datamodel.Beitragsgruppe(beitragsgruppe = u'Mitglied')
            newBeitragsgruppe.beitrag_nach_satzung = 50
            newBeitragsgruppe = datamodel.Beitragsgruppe(beitragsgruppe = u'Spender')
            newBeitragsgruppe.beitrag_nach_satzung = 0

        if len(datamodel.Suchkriterium.query.all()) == 0:
            newSuchkriterium = datamodel.Suchkriterium( \
                suchkriterium = u'ausgetretene Mitglieder verbergen')
            newSuchkriterium.abfrage = \
                '(austrittsdatum <= date(\'now\')) OR (austrittsdatum IS NULL)'
            # SQLite-Datumsfunktionen https://www.sqlite.org/lang_datefunc.html
            newSuchkriterium = datamodel.Suchkriterium( \
                suchkriterium = u'nur Mitglieder')
            newSuchkriterium.abfrage = \
                'id IN (SELECT id ' + \
                    'FROM mitglied ' + \
                    'WHERE mitgliedsgruppe_id = (' + \
                        'SELECT id ' + \
                        'FROM mitgliedsgruppe ' + \
                        'WHERE mitgliedsgruppe = \'Mitglied\'))'
            newSuchkriterium = datamodel.Suchkriterium( \
                suchkriterium = u'nur Spender')
            newSuchkriterium.abfrage = \
                'id IN (SELECT id ' + \
                    'FROM mitglied ' + \
                    'WHERE mitgliedsgruppe_id = (' + \
                        'SELECT id ' + \
                        'FROM mitgliedsgruppe ' + \
                        'WHERE mitgliedsgruppe = \'Spender\'))'
            newSuchkriterium = datamodel.Suchkriterium( \
                suchkriterium = u'mit Emailadresse')
            newSuchkriterium.abfrage = \
                'id IN (SELECT mitglied_id ' + \
                    'FROM emailadresse)'
            newSuchkriterium = datamodel.Suchkriterium( \
                suchkriterium = u'ohne Emailadresse')
            newSuchkriterium.abfrage = \
                'id NOT IN (SELECT mitglied_id ' + \
                    u'FROM emailadresse)'
            newSuchkriterium = datamodel.Suchkriterium( \
                suchkriterium = u'Überweiser')
            newSuchkriterium.abfrage = \
                u'zahlungsart_id = (SELECT id FROM zahlungsart ' + \
                    u'WHERE zalungsart = \'Überweisung\''

        elixir.session.commit() #speichern
        self.prepareCbxValues()

    @QtCore.pyqtSlot()
    def on_actSMTP_triggered(self):
        self.setSMTPSettings()

    @QtCore.pyqtSlot()
    def on_actOpen_triggered(self):
        dbfile = QtGui.QFileDialog.getOpenFileName(self, u"Mitgliederkartei öffnen",
            filter = "Mitgliederkartei (*.db)")
        if dbfile != "":
            self.initDb(dbfile)

    @QtCore.pyqtSlot()
    def on_actNeu_triggered(self):
        dbfile = QtGui.QFileDialog.getSaveFileName(self, u"Mitgliederkartei anlegen",
            filter = "Mitgliederkartei (*.db)")

        if dbfile != "":
            self.initDb(dbfile)

    @QtCore.pyqtSlot(name="on_actBeenden_triggered")
    def on_actBeenden_triggered(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_actMitgliedFinden_triggered(self):
        dlg = SucheDialog()
        dlg.show()
        result = dlg.exec_()

        if result == 1:
            pass
            #TODO: Filter neu setzen

    @QtCore.pyqtSlot(name="on_actMitgliedNeu_triggered")
    def on_actMitgliedNeu_triggered(self):
        newTab = QtGui.QWidget()
        self.newMemberId = self.newMemberId - 1
        newTab.setObjectName("neu")
        MemberData(self.db, self, \
                   newTab, self.newMemberId)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/identity_notsaved.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        newTitle = QtCore.QString("Neues Mitglied " + str(self.newMemberId * (-1)))
        idx = self.ui.tabMitglied.addTab(newTab, icon, newTitle)
        self.ui.tabMitglied.setCurrentIndex(idx)

    def initSchreiben(self,  titel = u"aussagefähiger Titel",  art = "Email",  theseMitglieder = None):
        newSchreiben = datamodel.Schreiben()
        newSchreiben.titel = titel
        newSchreiben.erzeugt = datetime.now()
        schreibenArt = datamodel.Schreibenart.get_by(schreibenart = art)

        if schreibenArt:
            newSchreiben.art = schreibenArt

        if not theseMitglieder:
            # Mitglieder hinzufügen
            selModel = self.ui.tblMitglieder.selectionModel()

            if len(selModel.selectedRows()) == 0: # keine Auswahl, also alle
                self.ui.tblMitglieder.selectAll()

            theseMitglieder = []

            for idx in selModel.selectedRows():
                thisMitgliedsnummer = self.memberModel.data(idx).toInt()[0]
                thisMitglied = datamodel.Mitglied.get_by(mitgliedsnummer = thisMitgliedsnummer)
                theseMitglieder.append(thisMitglied)

        if len(theseMitglieder) > 0:
            newSchreiben.mitglieder = theseMitglieder
        else:
            QtGui.QMessageBox.warning(None,u"keine Auswahl", u"Es wurden keine Adressaten ausgewählt!")
            elixir.session.rollback()
            return None

        return newSchreiben

    # arg thisText is QString("$mitgliedsname")
    def replacePlaceholders(self,  thisText,  thisMitgliedsnummer):
        isNaturalMember = True
        mitglieder = datamodel.MitgliedNatuerlich.query.filter_by(\
                                mitgliedsnummer=thisMitgliedsnummer).all()

        if len(mitglieder) == 0:
            isNaturalMember = False
            mitglieder = datamodel.MitgliedJuristisch.query.filter_by(\
                                mitgliedsnummer=thisMitgliedsnummer).all()

        if len(mitglieder) == 0:
            QtGui.QMessageBox.error(None, "", "Mitglied nicht gefunden")
            return None
        else:
            mitglied = mitglieder[0]

        #Daten aus DB einlesen
        if isNaturalMember:
            thisTitel = mitglied.titel
            thisNamenszusatz = mitglied.namenszusatz

            if not thisTitel:
                thisTitel = ""

            if not thisNamenszusatz:
                thisNamenszusatz = ""

            thisMitgliedsname = thisTitel + " " + mitglied.vorname + \
                " " + thisNamenszusatz + " " + mitglied.mitgliedsname

        else:
            thisMitgliedsname = mitglied.mitgliedsname
            thisAnsprechpartner = mitglied.ansprechpartner

            if thisAnsprechpartner != "":
                thisMitgliedsname += "<br>" + thisAnsprechpartner

        thisText.replace(QtCore.QString("$mitgliedsname"),  QtCore.QString(thisMitgliedsname))

        thisHnrZusatz = mitglied.hnrzusatz

        if not thisHnrZusatz:
            thisHnrZusatz = ""

        thisAdressZusatz = mitglied.adresszusatz
        thisAdresse = mitglied.strasse + " " + str(mitglied.hnr) + thisHnrZusatz  + "<br>"

        if thisAdressZusatz:
            thisAdresse = thisAdresse + thisAdressZusatz + "<br>"

        thisAdresse = thisAdresse + str(mitglied.ort.plz) + " " + mitglied.ort.ort
        thisText.replace(QtCore.QString("$adresse"),  QtCore.QString(thisAdresse))
        thisText.replace(QtCore.QString("$datum"),  QtCore.QDate.currentDate().toString("dd.MM.yyyy"))
        return thisText

    def replaceZahlungen(self,  thisText,  thisMitgliedsnummer,  thisYear):
        mitglieder = datamodel.MitgliedNatuerlich.query.filter_by(\
                                mitgliedsnummer=thisMitgliedsnummer).all()

        if len(mitglieder) == 0:
            mitglieder = datamodel.MitgliedJuristisch.query.filter_by(\
                                mitgliedsnummer=thisMitgliedsnummer).all()

        if len(mitglieder) == 0:
            QtGui.QMessageBox.error(None, "", "Mitglied nicht gefunden")
            return None
        else:
            mitglied = mitglieder[0]

        summe = None

        for zahlung in mitglied.zahlungen:
            if QtCore.QDate(zahlung.zahldatum).year() == thisYear:
                sList = QtCore.QString(str(zahlung.betrag)).split(".")
                thisSummeB = numberToWord.num2word(sList[0].toInt()[0])

                if len(sList) == 2 and sList[1].toInt()[0] > 0:
                    thisSummeB = thisSummeB + " Komma " + numberToWord.num2word(sList[1].toInt()[0])

                loc=QtCore.QLocale.system()

                if summe == None:
                    summe = loc.toString(zahlung.betrag)
                    summeB = thisSummeB
                    zahldatum = QtCore.QDate(zahlung.zahldatum).toString("dd.MM.yyyy")
                else:
                    summe += "</FONT></FONT></P>"
                    summe += "<P CLASS=\"western\"><FONT FACE=\"Liberation Sans, sans-serif\"><FONT SIZE=2>"
                    summe += loc.toString(zahlung.betrag)
                    summeB += "</FONT></FONT></P>"
                    summeB += "<P CLASS=\"western\"><FONT FACE=\"Liberation Sans, sans-serif\"><FONT SIZE=2>"
                    summeB += thisSummeB
                    zahldatum += "</FONT></FONT></P>"
                    zahldatum += "<P CLASS=\"western\"><FONT FACE=\"Liberation Sans, sans-serif\"><FONT SIZE=2>"
                    zahldatum += QtCore.QDate(zahlung.zahldatum).toString("dd.MM.yyyy")

        thisText.replace(QtCore.QString("$summe"),  QtCore.QString(summe))
        thisText.replace(QtCore.QString("$bsumme"),  QtCore.QString(summeB))
        thisText.replace(QtCore.QString("$zahldatum"),  QtCore.QString(zahldatum))

        return thisText

    @QtCore.pyqtSlot()
    def on_actLastschrift_triggered(self):
        selModel = self.ui.tblMitglieder.selectionModel()

        if len(selModel.selectedRows()) == 0: # keine Auswahl, also alle
            QtGui.QMessageBox.warning(None,u"keine Auswahl",
                u"Bitte alle Mitglieder auswählen, für die ein Brief zur Ankündigung einer Lastschrift gedruckt werden soll!")
        else:

            for idx in selModel.selectedRows():
                thisMitgliedsnummer = self.memberModel.data(idx).toInt()[0]
                thisMitglied = datamodel.Mitglied.get_by(mitgliedsnummer = thisMitgliedsnummer)

                if thisMitglied.zahlungsart.zahlungsart != "Bankeinzug":
                    QtGui.QMessageBox.warning(None,u"kein Bankeinzug",
                    u"Dieses Mitglied nimmt nicht am Bankeinzug teil!")
                    return None

                newSchreiben = self.initSchreiben(u"Ankündigung einer Lastschrift",  theseMitglieder = [thisMitglied])

                if newSchreiben:
                    vorlage = '/home/benno/verein/mitglied/vorlagen/ankuendigung_sepa.html'
                    try:
                        fh = QtCore.QFile(vorlage)
                        if not fh.open(QtCore.QIODevice.ReadOnly):
                            raise IOError(str(fh.errorString()))

                        stream = QtCore.QTextStream(fh)
                        stream.setCodec("UTF-8")
                        inhalt = stream.readAll()
                    #except IOError as e: # Python3
                    except IOError, e: # Python2
                        QtGui.QMessageBox.warning(self, "Load Error",
                        "Failed to load %s: %s" % (vorlage, e))

                    fh.close()
                    strMitgliedsnummer = str(thisMitgliedsnummer)
                    while len(strMitgliedsnummer) < 5:
                        strMitgliedsnummer = "0" + strMitgliedsnummer

                    inhalt.replace(QtCore.QString("$mandatsreferenz"),  QtCore.QString(strMitgliedsnummer))

                    thisAnrede = thisMitglied.anrede.anrede
                    anrede = "Liebe"

                    if thisAnrede == "Herr":
                        anrede += "r"

                    anrede += " " + thisMitglied.vorname + " " + thisMitglied.mitgliedsname
                    inhalt.replace(QtCore.QString("$anrede"),  QtCore.QString(anrede))

                    heute = QtCore.QDate.currentDate()
                    forYear = heute.year()
                    inhalt.replace(QtCore.QString("$jahr"),  QtCore.QString(str(forYear)))

                    targetDate = heute.addDays(14)
                    inhalt.replace(QtCore.QString("$datum"),  targetDate.toString("dd.MM.yyyy"))

                    beitrag = thisMitglied.individueller_beitrag

                    if beitrag == None:
                        beitrag = thisMitglied.beitragsgruppe.beitrag_nach_satzung

                    if QtCore.QDate(thisMitglied.eintrittsdatum) >= QtCore.QDate.fromString("01.07." + str(forYear),  "dd.MM.yyyy"):
                        beitrag = beitrag / 2

                    inhalt.replace(QtCore.QString("$betrag"),  QtCore.QString(str(beitrag)))
                    inhalt.replace(QtCore.QString("$iban"),  QtCore.QString(thisMitglied.iban))
                    inhalt.replace(QtCore.QString("$bic"),  QtCore.QString(thisMitglied.bic))
                    inhalt.replace(QtCore.QString("$bank"),  QtCore.QString(thisMitglied.bic))
                    newSchreiben.text = unicode(inhalt)
                    self.makeSchreiben(newSchreiben)

    @QtCore.pyqtSlot()
    def on_actSEPA_Umstellung_triggered(self):
        selModel = self.ui.tblMitglieder.selectionModel()

        if len(selModel.selectedRows()) == 0: # keine Auswahl, also alle
            QtGui.QMessageBox.warning(None,u"keine Auswahl",
                u"Bitte alle Mitglieder auswählen, für die ein Brief zur SEPA-Umstellung gedruckt werden soll!")
        else:

            for idx in selModel.selectedRows():
                thisMitgliedsnummer = self.memberModel.data(idx).toInt()[0]
                thisMitglied = datamodel.Mitglied.get_by(mitgliedsnummer = thisMitgliedsnummer)

                if thisMitglied.zahlungsart.zahlungsart != "Bankeinzug":
                    QtGui.QMessageBox.warning(None,u"kein Bankeinzug",
                    u"Dieses Mitglied nimmt nicht am Bankeinzug teil!")
                    return None

                newSchreiben = self.initSchreiben(u"SEPA-Umstellung",  theseMitglieder = [thisMitglied])

                if newSchreiben:
                    vorlage = '/home/benno/verein/mitglied/vorlagen/umstellung_sepa.html'
                    try:
                        fh = QtCore.QFile(vorlage)
                        if not fh.open(QtCore.QIODevice.ReadOnly):
                            raise IOError(str(fh.errorString()))

                        stream = QtCore.QTextStream(fh)
                        stream.setCodec("UTF-8")
                        inhalt = stream.readAll()
                    #except IOError as e: # Python3
                    except IOError, e: # Python2
                        QtGui.QMessageBox.warning(self, "Load Error",
                        "Failed to load %s: %s" % (vorlage, e))

                    fh.close()
                    strMitgliedsnummer = str(thisMitgliedsnummer)
                    while len(strMitgliedsnummer) < 5:
                        strMitgliedsnummer = "0" + strMitgliedsnummer

                    inhalt.replace(QtCore.QString("$mandatsreferenz"),  QtCore.QString(strMitgliedsnummer))

                    thisAnrede = thisMitglied.anrede.anrede
                    anrede = "Liebe"

                    if thisAnrede == "Herr":
                        anrede += "r"

                    anrede += " " + thisMitglied.vorname + " " + thisMitglied.mitgliedsname
                    inhalt.replace(QtCore.QString("$anrede"),  QtCore.QString(anrede))
                    inhalt.replace(QtCore.QString("$iban"),  QtCore.QString(thisMitglied.iban))
                    inhalt.replace(QtCore.QString("$bic"),  QtCore.QString(thisMitglied.bic))
                    newSchreiben.text = unicode(inhalt)
                    self.makeSchreiben(newSchreiben)

    @QtCore.pyqtSlot()
    def on_actSpendenbescheinigung_triggered(self):
        selModel = self.ui.tblMitglieder.selectionModel()

        if len(selModel.selectedRows()) == 0: # keine Auswahl, also alle
            QtGui.QMessageBox.warning(None,u"keine Auswahl",
                u"Bitte alle Mitglieder auswählen, für die eine Spendenbescheinigung gedruckt werden soll!")
        else:

            for idx in selModel.selectedRows():
                thisYear,  ok = QtGui.QInputDialog.getInt(None, "Spendenbescheinigung",  u"Ausstellungsjahr",
                                                     QtCore.QDate.currentDate().year() - 1)

                if not ok:
                    return None

                thisMitgliedsnummer = self.memberModel.data(idx).toInt()[0]
                thisMitglied = datamodel.Mitglied.get_by(mitgliedsnummer = thisMitgliedsnummer)
                newSchreiben = self.initSchreiben(u"Spendenbescheinigung",  "Brief",  [thisMitglied])

                if newSchreiben:
                    vorlage = '/home/benno/verein/mitglied/vorlagen/spendenbescheinigung.html'

                    try:
                        fh = QtCore.QFile(vorlage)
                        if not fh.open(QtCore.QIODevice.ReadOnly):
                            raise IOError(str(fh.errorString()))

                        stream = QtCore.QTextStream(fh)
                        stream.setCodec("UTF-8")
                        inhalt = stream.readAll()
                    #except IOError as e: # Python3
                    except IOError, e: # Python2
                        QtGui.QMessageBox.warning(self, "Load Error",
                        "Failed to load %s: %s" % (vorlage, e))

                    fh.close()
                    inhalt = self.replacePlaceholders(inhalt,  thisMitgliedsnummer)
                    inhalt = self.replaceZahlungen(inhalt,  thisMitgliedsnummer,  thisYear)
                    newSchreiben.text = unicode(inhalt)
                    self.makeSchreiben(newSchreiben, True,  None,  True)

    @QtCore.pyqtSlot()
    def on_actSchreibenVerfassen_triggered(self):
        newSchreiben = self.initSchreiben()

        if newSchreiben:
            self.makeSchreiben(newSchreiben, True)

    @QtCore.pyqtSlot()
    def on_actDatenblatt_triggered(self):
        newSchreiben = datamodel.Schreiben()
        newSchreiben.titel = u"Willkommen im Kaleidoskop e.V."
        newSchreiben.erzeugt = datetime.now()
        selModel = self.ui.tblMitglieder.selectionModel()

        if len(selModel.selectedRows()) != 1:
            QtGui.QMessageBox.information(None, "",
                u"Bitte das Mitglied auswählen, für das das Datenblatt erzeugt werden soll")
            return None

        idx = selModel.selectedRows()[0]
        thisMitgliedsnummer = self.memberModel.data(idx).toInt()[0]
        thisMitglied = datamodel.Mitglied.get_by(mitgliedsnummer = thisMitgliedsnummer)

        newSchreiben.mitglieder = [thisMitglied]
        natMitglied = self.isNaturalMember(thisMitgliedsnummer)

        if natMitglied:
            if thisMitglied.anrede.anrede == "Frau":
                thisText = u"Sehr geehrte Frau"
            else:
                thisText = u"Sehr geehrter Herr"

            if thisMitglied.titel != None:
                thisText += " " + thisMitglied.titel

            if thisMitglied.namenszusatz != None:
                thisText += " " + thisMitglied.namenszusatz

            thisText += " " + thisMitglied.mitgliedsname + ","
        else:
            thisText = u"Sehr geehrter " + thisMitglied.ansprechpartner + ","

        thisText += u"\n\nSie sind dem Kaleidoskop e.V. beigetreten. " + \
            u"Da laut Satzung der Vorstand über die Aufnahme der Mitglieder entscheidet, "+ \
            u"hat sich die Aufnahme leider bis nach der letzten Vorstandssitzung verzögert. \nWir haben folgende Daten von Ihnen erfasst:"
        thisText = thisText + u"\n\n1) Stammdaten"
        thisText = thisText + u"\nMitgliedsnummer: " + str(thisMitgliedsnummer) + "\n"

        if  natMitglied:
            thisText = thisText + thisMitglied.anrede.anrede

            if thisMitglied.titel:
                thisText = thisText + u" " + thisMitglied.titel

            thisText = thisText + u" " + thisMitglied.vorname + " "

        thisText = thisText + thisMitglied.mitgliedsname

        if natMitglied:

            if thisMitglied.namenszusatz:
                thisText = thisText + u", " + thisMitglied.namenszusatz

            thisText = thisText + u"\nGeburtsdatum: " + str(QtCore.QDate(thisMitglied.geburtsdatum).toString("dd.MM.yyyy"))

            if thisMitglied.beruf:
                thisText = thisText + u"\nBeruf: " + thisMitglied.beruf
        else:
            if thisMitglied.ansprechpartner:
                thisText = thisText + u"\nAnsprechpartner: " + thisMitglied.ansprechpartner

        if thisMitglied.hinweise:
            thisText = thisText + u"\nSonstiges: " + thisMitglied.hinweise

        thisText = thisText + u"\n\n2) Anschrift"

        if thisMitglied.adresszusatz:
            thisText = thisText + "\n" + thisMitglied.adresszusatz

        thisText = thisText + "\n" + thisMitglied.strasse + " " + str(thisMitglied.hnr)

        if thisMitglied.hnrzusatz:
            thisText = thisText + thisMitglied.hnrzusatz

        thisText = thisText + "\n" + thisMitglied.ort.land.kuerzel + " - " + thisMitglied.ort.plz + " " + thisMitglied.ort.ort

        thisText = thisText + u"\n\n3) Kontaktdaten"
        noEmail = True

        for emailAdresse in thisMitglied.emailadressen:
            noEmail = False
            thisText = thisText + u"\nEmail-Adresse (" + emailAdresse.hinweis.hinweis + "): " + \
                emailAdresse.emailadresse

        for telefonFax in thisMitglied.telefonfaxnummern:
            thisText = thisText + u"\n" + telefonFax.hinweis.hinweis + \
                ": " + telefonFax.telefonfax

        thisText = thisText + u"\n\n4) Mitgliedschaft"
        thisText = thisText + u"\nMitgliedsgruppe: " + thisMitglied.mitgliedsgruppe.mitgliedsgruppe
        thisText = thisText + u"\neingetreten am: " + str(QtCore.QDate(thisMitglied.eintrittsdatum).toString("dd.MM.yyyy"))

        thisText = thisText + u"\n\n5) Beitragszahlung"
        beitrag = thisMitglied.individueller_beitrag

        if not beitrag:
            beitrag = thisMitglied.beitragsgruppe.beitrag_nach_satzung

        thisText = thisText + u"\nJahresbeitrag: " + str(beitrag) + " EUR"
        thisText = thisText + u"\nZahlweise: " + thisMitglied.zahlweise.zahlweise
        thisText = thisText + u"\nZahlungsart: " + thisMitglied.zahlungsart.zahlungsart

        if thisMitglied.zahlungsart.zahlungsart == u"Bankeinzug":
            thisText = thisText + u"\nBankverbindung:"
            thisText = thisText + u"\nIBAN: " + str(thisMitglied.iban)
            thisText = thisText + "\nBIC: " + str(thisMitglied.bic)
            thisText = thisText + u"\nKontoinhaber: " + thisMitglied.kontoinhaber
            thisText = thisText + u"\nEinzugsermächtigung vom: " + str(QtCore.QDate(thisMitglied.einzugsermaechtigungsdatum).toString("dd.MM.yyyy"))

        thisText = thisText + u"\n\nBitte überprüfen Sie Ihre Daten und " + \
            u"teilen Sie eventuelle Unrichtigkeiten baldmöglichst mit.\n\n"

        if thisMitglied.mitgliedsgruppe.mitgliedsgruppe == u"Fördermitglied":
            thisText += u"Sie haben auf Ihrem Aufnahmeantrag \"Fördermitglied\" angekreuzt. " + \
                u"Ein Fördermitglied ist an der Mitgliederversammlung nicht stimmberechtigt. " + \
                u"Sie können die Fördermitgliedschaft jederzeit in eine \"normale\" Mitgliedschaft ändern.\n\n"

        thisText +=  u"Die Daten werden nur für vereinsinterne Zwecke gespeichert und nicht an Dritte weitergegeben.\n\n" + \
            u"mit besten Grüßen\n\n" + \
            u"Bernhard Ströbl"

        newSchreiben.text = thisText
        self.makeSchreiben(newSchreiben, True,  None,  noEmail)

    @QtCore.pyqtSlot()
    def on_actSpeicherpfad_triggered(self):
        speicherpfad = self.getPathSettings()

        if not speicherpfad:
            speicherpfad = QtCore.QString()

        speicherpfad = QtGui.QFileDialog.getExistingDirectory(None,
            u"Pfad zum Speichern von Schreiben auswählen", speicherpfad)

        if speicherpfad:
            settings = QtCore.QSettings() #u"Verein", u"Mitgliederverwaltung")
            settings.beginGroup(u"documentpath")
            settings.setValue("speicherpfad", speicherpfad)
            settings.endGroup()


    @QtCore.pyqtSlot(int, name="on_tabMitglied_tabCloseRequested")
    def on_tabMitglied_tabCloseRequested(self, thisTabIndex):
        thisTab = self.ui.tabMitglied.widget(thisTabIndex)

        if thisTabIndex == self.ui.tabMitglied.currentIndex():
            # zu schliessender Tab ist geöffneter Tab
            memberData = thisTab.childAt(1, 1)
        else:
            memberData = thisTab.childAt(1, 1).parentWidget().parentWidget()
            # position 1,1 is a button in the butttonBox

        if memberData.on_memberTabCloseRequested():
            self.ui.tabMitglied.removeTab(thisTabIndex)

def main():
    app = QtGui.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec_())

def openFileInApplication( fileName ):
    if os.path.exists( fileName ):
        if os.name == 'nt': # Window$
            os.startfile( fileName )
            return 1
        elif os.name == 'posix': # e.g. linux
            subprocess.call([ 'xdg-open', fileName ])
            return 1
        else:
            return 0
    else:
        return 0

if __name__ == "__main__":
    main()


    if ok:
        #generator = BildReportGenerator()
        #pdf = generator.generate([db])
        fsgenerator = FSReportGenerator()
        pdf = fsgenerator.generate([db, 3, unicode('Streuobstwiesää')])
        #testen
        #rtf = fsgenerator.generate([db, 3, streuobstwiese], output_type = 'rtf')

        #QtGui.QMessageBox.information(None,"", pdf)
        tempFile = tempfile.mkstemp(".pdf","qgsrprt")
        tempFileName = tempFile[1]
        os.close(tempFile[0])
        outfile = open(tempFileName, 'wb')
        outfile.write(pdf)
        outfile.close()
        openFileInApplication(tempFileName)
