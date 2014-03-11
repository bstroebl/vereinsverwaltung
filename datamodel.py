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

import elixir

class Anrede(elixir.Entity):
    elixir.using_options(tablename = 'anrede')
    #elixir.using_table_options(schema = 'schemaname')
    id = elixir.Field(elixir.Integer, primary_key = True)
    anrede = elixir.Field(elixir.Unicode(64), required = True)
    mitglieder = elixir.OneToMany('MitgliedNatuerlich')

    def __repr__(self):
        return '<Anrede "%s">' % (self.anrede)

class Austrittsgrund(elixir.Entity):
    elixir.using_options(tablename = 'austrittsgrund')
    id = elixir.Field(elixir.Integer, primary_key = True)
    austrittsgrund = elixir.Field(elixir.Unicode(255), required = True)
    mitglieder = elixir.OneToMany('Mitglied')

    def __repr__(self):
        return '<Austrittsgrund "%s">' % (self.austrittsgrund)

class Bank(elixir.Entity):
    elixir.using_options(tablename = 'bank')
    blz = elixir.Field(elixir.Integer, primary_key = True)
    bank = elixir.Field(elixir.Unicode(255), required = True)
    mitglieder = elixir.OneToMany('Mitglied')

    def __repr__(self):
        return '<Bank "%s" (BLZ "%s")>' % (self.bank, self.blz)

class Beitragsgruppe(elixir.Entity):
    elixir.using_options(tablename = 'beitragsgruppe')
    id = elixir.Field(elixir.Integer, primary_key = True)
    beitragsgruppe = elixir.Field(elixir.Unicode(255), required = True)
    beitrag_nach_satzung = elixir.Field(elixir.Integer)
    mitglieder = elixir.OneToMany('Mitglied')

    def __repr__(self):
        return '<Beitragsgruppe "%s" (Beitrag "%s")>' % \
            (self.beitragsgruppe, self.beitrag_nach_satzung)

class EmailAdresse(elixir.Entity):
    elixir.using_options(tablename = 'emailadresse')
    id = elixir.Field(elixir.Integer, primary_key = True)
    mitglied = elixir.ManyToOne('Mitglied')
    emailadresse = elixir.Field(elixir.Unicode(255), required = True)
    hinweis = elixir.ManyToOne('HinweisEmail')
    fehler = elixir.OneToMany('EmailFehler')

    def __repr__(self):
        return '<EmailAdresse "%s">' % (self.emailadresse)

class EmailFehler(elixir.Entity):
    elixir.using_options(tablename = 'emailfehler')
    id = elixir.Field(elixir.Integer, primary_key = True)
    fehler = elixir.Field(elixir.Unicode(255), required = True)
    fehlerdatum = elixir.Field(elixir.Date, required = True)
    email = elixir.ManyToOne('EmailAdresse')

    def __repr__(self):
        return '<EmailFehler "%s" vom "%s">' % (self.fehler, str(self.fehlerdatum))

class Land(elixir.Entity):
    elixir.using_options(tablename = 'land')
    id = elixir.Field(elixir.Integer, primary_key = True)
    land = elixir.Field(elixir.Unicode(255), required = True)
    kuerzel = elixir.Field(elixir.Unicode(3), required = True)
    orte = elixir.OneToMany('Ort')

    def __repr__(self):
        return '<Land "%s">' % (self.land)

class HinweisEmail(elixir.Entity):
    elixir.using_options(tablename = 'hinweis_email')
    id = elixir.Field(elixir.Integer, primary_key = True)
    hinweis = elixir.Field(elixir.Unicode(255), required = True)
    emailadressen = elixir.OneToMany('EmailAdresse')

    def __repr__(self):
        return '<HinweisEmail "%s">' % (self.hinweis)

class HinweisTelefonFax(elixir.Entity):
    elixir.using_options(tablename = 'hinweis_telefonfax')
    id = elixir.Field(elixir.Integer, primary_key = True)
    hinweis = elixir.Field(elixir.Unicode(255), required = True)
    telefonfax = elixir.OneToMany('TelefonFax')

    def __repr__(self):
        return '<HinweisTelefonFax "%s">' % (self.hinweis)

class HinweisZahlung(elixir.Entity):
    elixir.using_options(tablename = 'hinweis_zahlung')
    id = elixir.Field(elixir.Integer, primary_key = True)
    hinweis = elixir.Field(elixir.Unicode(255), required = True)
    zahlungen = elixir.OneToMany('Zahlung')

    def __repr__(self):
        return '<HinweisZahlung "%s">' % (self.hinweis)

class Mitglied(elixir.Entity):
    elixir.using_options(tablename = 'mitglied', inheritance = 'multi')
    mitgliedsnummer = elixir.Field(elixir.Integer, primary_key = True, colname = 'id')
    mitgliedsname = elixir.Field(elixir.Unicode(255), required = True)
    vorname = elixir.Field(elixir.Unicode(255), required = True)
    hinweise = elixir.Field(elixir.Unicode(255),  required = False)
    mitgliedsgruppe = elixir.ManyToOne('Mitgliedsgruppe')
    eintrittsdatum = elixir.Field(elixir.Date, required = True)
    letzte_aenderung = elixir.Field(elixir.TIMESTAMP, required = True)
    beitragsgruppe = elixir.ManyToOne('Beitragsgruppe')
    individueller_beitrag = elixir.Field(elixir.Integer)
    austrittsdatum = elixir.Field(elixir.Date)
    austrittsgrund = elixir.ManyToOne('Austrittsgrund')
    strasse = elixir.Field(elixir.Unicode(255), required = True)
    hnr = elixir.Field(elixir.Integer, required = True)
    hnrzusatz = elixir.Field(elixir.Unicode(8))
    adresszusatz = elixir.Field(elixir.Unicode(64))
    ort = elixir.ManyToOne('Ort')
    zahlungsart = elixir.ManyToOne('Zahlungsart')
    zahlweise = elixir.ManyToOne('Zahlweise')
    einzugsermaechtigungsdatum = elixir.Field(elixir.Date)
    kontonummer = elixir.Field(elixir.Integer)
    kontoinhaber = elixir.Field(elixir.Unicode(255))
    bank = elixir.ManyToOne('Bank')
    iban = elixir.Field(elixir.Unicode(32))
    bic = elixir.Field(elixir.Unicode(16))
    emailadressen = elixir.OneToMany('EmailAdresse')
    telefonfaxnummern = elixir.OneToMany('TelefonFax')
    zahlungen = elixir.OneToMany('Zahlung')
    schreiben = elixir.ManyToMany('Schreiben')

    def __repr__(self):
        return '<Mitglied "%s">' % (unicode(self.mitgliedsname))

class MitgliedJuristisch(Mitglied):
    '''child class of Mitglied, inheritance=multi: extra table for parent and child'''
    elixir.using_options(tablename = 'mitglied_juristisch', inheritance = 'multi')
    ansprechpartner = elixir.Field(elixir.Unicode(255), required = True)

    def __repr__(self):
        return '<Juristisches Mitglied "%s Ansprechpartner "%s">' % \
            (self.mitgliedsname, self.ansprechpartner)

class MitgliedNatuerlich(Mitglied):
    '''child class of Mitglied, inheritance=multi: extra table for parent and child'''
    elixir.using_options(tablename = 'mitglied_natuerlich', inheritance = 'multi')
    anrede = elixir.ManyToOne('Anrede')
    titel = elixir.Field(elixir.Unicode(255))
    namenszusatz = elixir.Field(elixir.Unicode(255))
    geburtsdatum = elixir.Field(elixir.Date, required = True)
    beruf = elixir.Field(elixir.Unicode(255))
    hauptmitglied = elixir.ManyToOne('MitgliedNatuerlich')
    abhaengigeMitglieder = elixir.OneToOne('MitgliedNatuerlich')

    def __repr__(self):
        return '<Natuerliches Mitglied "%s "%s" "%s">' % \
            (self.anrede, unicode(self.vorname), unicode(self.mitgliedsname))

class Mitgliedsgruppe(elixir.Entity):
    elixir.using_options(tablename = 'mitgliedsgruppe')
    id = elixir.Field(elixir.Integer, primary_key = True)
    mitgliedsgruppe = elixir.Field(elixir.Unicode(255), required = True)
    mitglieder = elixir.OneToMany('Mitglied')

    def __repr__(self):
        return '<Mitgliedsgruppe "%s">' % (self.mitgliedsgruppe)

class Ort(elixir.Entity):
    elixir.using_options(tablename = 'ort')
    id = elixir.Field(elixir.Integer, primary_key = True)
    ort = elixir.Field(elixir.Unicode(255), required = True)
    plz = elixir.Field(elixir.Unicode(8), required = True)
    land = elixir.ManyToOne('Land')
    mitglieder = elixir.OneToMany('Mitglied')

    def __repr__(self):
        return '<Ort "%s" "%s">' % (self.plz, self.ort)

class Schreiben(elixir.Entity):
    elixir.using_options(tablename = 'schreiben')
    id = elixir.Field(elixir.Integer, primary_key = True)
    mitglieder = elixir.ManyToMany('Mitglied')
    erzeugt = elixir.Field(elixir.TIMESTAMP, required = True)
    titel = elixir.Field(elixir.Unicode(255), required = True)
    text = elixir.Field(elixir.Text) #, convert_unicode = True)
    art = elixir.ManyToOne('Schreibenart')
    anhaenge = elixir.OneToMany('Schreibenanhang')

    def __repr__(self):
        return '<Schreiben "%s" vom "%s">' % (self.titel, str(self.erzeugt))

class Schreibenanhang(elixir.Entity):
    elixir.using_options(tablename = 'schreibenanhang')
    id = elixir.Field(elixir.Integer, primary_key = True)
    pfad = elixir.Field(elixir.Unicode(255), required = True)
    schreiben = elixir.ManyToOne('Schreiben')

    def __repr__(self):
        return '<Schreibenanhang "%s">' % (self.pfad)

class Schreibenart(elixir.Entity):
    elixir.using_options(tablename = 'schreibenart')
    id = elixir.Field(elixir.Integer, primary_key = True)
    schreibenart = elixir.Field(elixir.Unicode(255), required = True)
    schreiben = elixir.OneToMany('Schreiben')

    def __repr__(self):
        return '<Schreibenart "%s">' % (self.schreibenart)

class Suchkriterium(elixir.Entity):
    elixir.using_options(tablename = 'suchkriterium')
    id = elixir.Field(elixir.Integer, primary_key = True)
    suchkriterium = elixir.Field(elixir.Unicode(255), required = True)
    abfrage = elixir.Field(elixir.Unicode(1024), required = True)

    def __repr__(self):
        return '<Suchkriterium "%s">' % (self.suchkriterium)


class TelefonFax(elixir.Entity):
    elixir.using_options(tablename = 'telefonfax')
    id = elixir.Field(elixir.Integer, primary_key = True)
    mitglied = elixir.ManyToOne('Mitglied')
    telefonfax = elixir.Field(elixir.Unicode(255), required = True)
    hinweis = elixir.ManyToOne('HinweisTelefonFax')

    def __repr__(self):
        return '<TelefonFax "%s">' % (self.telefonfax)

class Zahlung(elixir.Entity):
    elixir.using_options(tablename = 'zahlung')
    id = elixir.Field(elixir.Integer, primary_key = True)
    mitglied = elixir.ManyToOne('Mitglied')
    betrag = elixir.Field(elixir.Float, required = True)
    zahldatum = elixir.Field(elixir.Date, required = True)
    hinweis = elixir.ManyToOne('HinweisZahlung')

    def __repr__(self):
        return '<Zahlung "%s" am "%s">' % (self.betrag, self.zahldatum)

class Zahlungsart(elixir.Entity):
    elixir.using_options(tablename = 'zahlungsart')
    id = elixir.Field(elixir.Integer, primary_key = True)
    zahlungsart = elixir.Field(elixir.Unicode(255), required = True)
    mitglieder = elixir.OneToMany('Mitglied')

    def __repr__(self):
        return '<Zahlungsart "%s">' % (self.zahlungsart)

class Zahlweise(elixir.Entity):
    elixir.using_options(tablename = 'zahlweise')
    id = elixir.Field(elixir.Integer, primary_key = True)
    zahlweise = elixir.Field(elixir.Unicode(255), required = True)
    mitglieder = elixir.OneToMany('Mitglied')

    def __repr__(self):
        return '<Zahlweise "%s">' % (self.zahlweise)

def main():
    elixir.metadata.bind = 'postgresql://verein:verein@127.0.0.1/elixir'
    elixir.metadata.bind.echo = True
    elixir.setup_all() # Verbindung aufbauen
    #elixir.create_all() # Tabellen anlegen
    #ort = Ort.query.all()[0]
    ort = Ort(ort = "Jena", plz = "07745")
    land = Land.query.first()
    ort.land = land
    id = ort.id
    anreden = Anrede.query.order_by(\
                   Anrede.anrede).all(),

    #for item in result:
    #    print item.mitgliedsname
    #    print item.letzte_aenderung
    b=elixir.session.commit()
    elixir.session.close()
if __name__ == "__main__":
    main()

