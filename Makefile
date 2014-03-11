# Makefile for a PyQGIS plugin 

#pyrcc4 

#pyuic4 ./tools/editor.ui -o ./tools/editor.py
pyuic4 ./Ui_MainWindow.ui -o ./Ui_MainWindow.py
pyuic4 ./Ui_Mitglied.ui -o ./Ui_Mitglied.py
pyuic4 ./Ui_MitgliedNatuerlich.ui -o ./Ui_MitgliedNatuerlich.py
pyuic4 ./Ui_MitgliedJuristisch.ui -o ./Ui_MitgliedJuristisch.py
pyuic4 ./Ui_LookupTable.ui -o ./Ui_LookupTable.py
pyuic4 ./Ui_Verbindung.ui -o ./Ui_Verbindung.py
pyuic4 ./Ui_SMTP.ui -o ./Ui_SMTP.py
pyuic4 ./Ui_Schreiben.ui -o ./Ui_Schreiben.py
pyuic4 ./Ui_Suche.ui -o ./Ui_Suche.py
pyrcc4 ./resources.qrc -o ./resources_rc.py
