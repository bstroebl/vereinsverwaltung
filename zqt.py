# -*- coding: utf-8 -*-
"""
/***************************************************************************
zutils.zqt
Utilities for qt in QGIS plugins
                             -------------------
begin                : 2010-08-11
copyright            : (C) 2010 by Bernhard Stroebl, KIJ/DV
email                : bernhard.stroebl@jena.de
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

from PyQt4 import QtCore, QtGui, QtSql

class QListWidgetItemId( QtGui.QListWidgetItem ):
    def __init__( self, displayString, id = None ):
        QtGui.QListWidgetItem.__init__( self, displayString )
        self.id = id
    def setId( self, id ):
        self.id = id

# Quelle: http://www.opensubscriber.com/message/pyqt@riverbankcomputing.com/13980971.html
class TreeItem( object ):
    def __init__( self, data, parent = None ):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild( self, item ):
        self.childItems.append( item )

    #<Benno>
    def removeChild( self, row ):
        if self.childCount <= row:
            child = self.child( row )
            childItems.pop( row )
            return child
        else:
            return None
    #</Benno>

    def child( self, row ):
        return self.childItems[ row ]

    def childCount( self ):
        return len( self.childItems )

    def columnCount( self ):
        return len( self.itemData )

    def data( self, column ):
        try:
            return self.itemData[ column ]
        except IndexError:
            return None

    def parent( self ):
        return self.parentItem

    def row( self ):
        if self.parentItem:
            return self.parentItem.childItems.index( self )

        return 0


# fields: 0: parent_id, 1: parent_name, 2: child_id, all others are child fields to fill in
# columns in treeWidget, number of columns is changed accordingly
# treeWidget: to be filled
# db: QSqlDatabase object
# numFields: int Anzahl der übergebenen Felder (min 4)
# selectStatement, Bsp. SELECT parent_id, parent_name, child_id, child_name1, child_name2 FROM some_table WHERE parent_id = :id;
# id: int; the id for the WHERE statement
# headers: List
# returns 0 error 1 success
def fillTreeQt( treeWidget, db, numFields, selectStatement, id, headers = None ):
    # how many columns are needed?
    treeWidget.setColumnCount( numFields - 3 )

    if headers:
        treeWidget.setHeaderHidden( False )
        headerList = QtCore.QStringList()

        for header in headers:
            headerList.append( header )

        treeWidget.setHeaderLabels( headerList )
    else:
        treeWidget.setHeaderHidden( True )

    if db:
        query = QtSql.QSqlQuery( db )
        query.prepare( selectStatement )
        query.bindValue( ":id", QtCore.QVariant( id ))
        query.exec_()

        if query.isActive():
            treeWidget.clear()
            lastParent = ""

            while query.next(): # returns false when all records are done
                parentId = int( query.value(0).toString() )
                parent = query.value(1).toString()
                childId = int( query.value(2).toString() )

                resultList = QtCore.QStringList()

                for i in range( 3, numFields ):
                    resultList.append( query.value(i).toString() )

                if parent != lastParent:
                    parentItem = treeAddParentItem(treeWidget, parentId, parent)
                    lastParent = parent

                treeAddChildItem(parentItem, childId, resultList)

            query.finish()
            return 1
        else:
            QtGui.QMessageBox.warning( None, "Database Error", \
                QtCore.QString( "%1 \n %2" ).arg( query.lastError().text()).arg( query.lastQuery() ) )
            return 0
    else:
        return 0


def treeRemoveParentItem(treeWidget, thisItem):
    parentId = thisItem.parentId

    for i in range(treeWidget.topLevelItemCount()):

        if treeWidget.topLevelItem(i) == thisItem:
            treeWidget.takeTopLevelItem(i)
            return True

    return False # not Found

def treeRemoveChildItem(treeWidget, thisItem):
    parentItem = thisItem.parent()
    parentItem.removeChild(thisItem)
    return True

def treeRemoveItem(treeWidget, thisItem):
    parentId = thisItem.parentId
    childId = thisItem.childId

    if parentId:
        return treeRemoveParentItem(treeWidget, thisItem)
    if childId:
        return treeRemoveChildItem(treeWidget, thisItem)

def treeAddParentItem(treeWidget, parentId, parent):
    parentItem = QtGui.QTreeWidgetItem(QtCore.QStringList(parent))
    parentItem.parentId = parentId
    parentItem.childId = None
    treeWidget.addTopLevelItem(parentItem)
    return parentItem

'''parentItem: QTreeWidgetItem
childId: int
child: QString'''
def treeAddChildItem(parentItem, childId, child):
    childItem = QtGui.QTreeWidgetItem(QtCore.QStringList(child))
    childItem.parentId = None
    childItem.childId = childId
    parentItem.addChild(childItem)
    return childItem

# fields in SELECT-statement: 0: parent_id, 1: parent_name, 2: checked (integer: 0 unchecked, 2: checked)
# listWidget: to be filled
# db: QSqlDatabase object
# selectStatement: SELECT r.featureId_Field,
#                               r.itemId_Field,
#                               CASE COALESCE( lnk.featureId_Field, 0 ) WHEN 0 THEN 0 ELSE 2 END as checked
#                           FROM schema.itemTable r
#                               LEFT JOIN (SELECT * FROM schema.table1_has_table2 WHERE featureId_Field = :featureId) lnk ON r.itemId_Field = lnk.itemId_Field
#                           ORDER BY was auch immer;
# featureId: int; the id
# headers: List
# returns 0 error 1 success
def fillMultiChoice( listWidget, db, selectStatement, featureId ):
    # how many columns are needed?
    #QtGui.QMessageBox.information(None,'fillMultiChoice',selectStatement)
    if db:
        query = QtSql.QSqlQuery( db )
        query.prepare( selectStatement )
        query.bindValue( ":featureId", QtCore.QVariant( featureId ))
        query.exec_()

        if query.isActive():
            listWidget.clear()

            while query.next(): # returns false when all records are done
                parentId = int( query.value(0).toString() )
                parent = unicode( query.value(1).toString() )
                checked = int( query.value(2).toString() )
                #QtGui.QMessageBox.information(None,"debug",str(parentId) + ": " + parent + " checked = " + str(checked))
                parentItem = QListWidgetItemId( QtCore.QString( parent ))
                parentItem.setId( parentId )
                parentItem.setCheckState( checked )
                listWidget.addItem( parentItem )
            query.finish()
            return 1
        else:
            QtGui.QMessageBox.warning( None, "Database Error: fillMultiChoice", \
                QtCore.QString( "%1 \n %2" ).arg( query.lastError().text()).arg( query.lastQuery() ) )
            return 0
    else:
        return 0


# listWidget:  filled with fillMultiChoice()
# db: QSqlDatabase object
# deleteStatement: DELETE FROM schema.table1_has_table2 WHERE featureId_Field = :featureId;
# insertStatement: INSERT INTO schema.table1_has_table2 (featureId_Field, itemId_Field)  VALUES (:featureId, :itemId);
# featureId: int; the id
# returns 0 error 1 success
# first deletes all entries, then enters all checked entries
def saveMultiChoice( listWidget, db, deleteStatement, insertStatement, featureId ):
    if db:
        if db.transaction(): #start a transaction
            deleteQuery = QtSql.QSqlQuery( db )
            deleteQuery.prepare( deleteStatement )
            deleteQuery.bindValue( ":featureId", QtCore.QVariant( featureId ))
            deleteQuery.exec_()

            if deleteQuery.isActive():

                for i in range( listWidget.count() ):
                    item = listWidget.item( i )

                    if item.checkState() == 2:
                        itemId = item.id
                        insertQuery = QtSql.QSqlQuery( db )
                        insertQuery.prepare( insertStatement )
                        insertQuery.bindValue( ":featureId", QtCore.QVariant( featureId ))
                        insertQuery.bindValue( ":itemId", QtCore.QVariant( itemId ))
                        insertQuery.exec_()

                        if insertQuery.isActive():
                            insertQuery.finish()
                        else:
                            QtGui.QMessageBox.warning( None, "Database Error: saveMultiChoice", \
                                QtCore.QString( "%1 \n %2" ).arg( insertQuery.lastError().text()).arg( insertQuery.lastQuery() ) )
                            return 0
                return 1
            else:
                QtGui.QMessageBox.warning( None, "Database Error: saveMultiChoice", \
                    QtCore.QString( "%1 \n %2" ).arg( deleteQuery.lastError().text()).arg( deleteQuery.lastQuery() ) )
                return 0
    else:
        return 0


# function to fill a comboBox with the values from a lookup table
# cbx: QComboBox
# db: QSqlDatabase object
# selectStatement with 2 fields: 1: displayField , 2 [optional] keyField
# returns 0 error 1 success
def fillComboBoxQt( cbx, db, selectStatement, insertNull = False ):

    if db:
        query = QtSql.QSqlQuery( db )
        query.prepare( selectStatement )
        query.exec_()

        if query.isActive():
            cbx.clear()

            if insertNull:
                cbx.addItem("", -9999)

            while query.next(): # returns false when all records are done
                sValue = QtCore.QString( query.value(0).toString() )

                if query.value(1):
                    keyValue = query.value(1)
                    cbx.addItem( sValue, keyValue )
                else:
                    cbx.addItem( sValue )

            query.finish()
            return 1
        else:
            QtGui.QMessageBox.warning( None, "Database Error: fillComboBoxQt", \
                QtCore.QString( "%1 \n %2" ).arg( query.lastError().text()).arg( query.lastQuery() ) )
            return 0
    else:
        return 0

# function to fill a comboBox from an XML QDomNode
# cbx: QComboBox
# rootNode: QDomNode
# example
# <node>
#   <value id="2">Anzeigewert2</value>
#   <value id="1">Anzeigewert1</value>
# </node>
# returns 0 error 1 success
def fillComboBoxFromXml(cbx, thisNode, insertNull = False):

    if insertNull:
        cbx.addItem("", -9999)

    for i in range(thisNode.childNodes().count()):
        aNode = thisNode.childNodes().item(i)
        atts = aNode.attributes()
        sValue = aNode.firstChild().nodeValue() # retrieve text from a TextNode
        keyValue = int(str(atts.namedItem(QtCore.QString("id")).nodeValue()))
        cbx.addItem( sValue, keyValue )
    return 1


# function to fill a comboBox with the values from a query
# cbx: QComboBox
# query: QtSql.QSqlQuery  selectStatement with 2 fields: 1: displayField , 2 [optional] keyField
# returns 0 error 1 success
def fillComboBoxFromQuery( cbx, query):

    if query:
        query.exec_()

        if query.isActive():
            cbx.clear()

            while query.next(): # returns false when all records are done
                sValue = QtCore.QString( query.value(0).toString() )

                if query.value(1):
                    keyValue = query.value(1)
                    cbx.addItem( sValue, keyValue )
                else:
                    cbx.addItem( sValue )

            query.finish()
            return 1
        else:
            QtGui.QMessageBox.warning( None, "Database Error: fillComboBoxQt", \
                QtCore.QString( "%1 \n %2" ).arg( query.lastError().text()).arg( query.lastQuery() ) )
            return 0
    else:
        return 0

#sets the currentIndex to the value corresponding to int
# Arg 0: QComboBox
# Arg 1: integer
def cbxValueFromInt( cbx, int ):
    for i in range( cbx.count() ):
        if cbx.itemData( i ) == int:
            cbx.setCurrentIndex( i )
            break

#sets the currentIndex to the value corresponding to text
# Arg 0: QComboBox
# Arg 1: string
def cbxValueFromText( cbx, thisText ):
    for i in range( cbx.count() ):
        if cbx.itemText( i ) == thisText:
            cbx.setCurrentIndex( i )
            break

# Connection between a txl and a cbx in a FormHelper
# sets cbx's value to the Value contained in txl
# cbx QComboBox
# txl QLineEdit
def cbxValueFromTxlInt( cbx, txl ):
    for i in range( cbx.count() ):
        if cbx.itemData( i ).toString() == txl.text():
            cbx.setCurrentIndex( i )
            break

# Connection between a txl and a cbx in a FormHelper
# sets cbx's value to the Value contained in txl
# cbx QComboBox
# txl QLineEdit
def cbxValueFromTxlText( cbx, txl ):
    for i in range( cbx.count() ):
        if cbx.itemText( i ) == txl.text():
            cbx.setCurrentIndex( i )
            break

def formatInt( txl ):
    s = txl.text()

    if s == '':
        return QtCore.QVariant()
    else:
        return QtCore.QVariant( s )

def formatFloat( txl ):
    s = txl.text()

    if s == '':
        return QtCore.QVariant()
    elif s == '.':
        return QtCore.QVariant()
    else:
        return QtCore.QVariant( s )

# returns the max value in idField (String) in a table with tableName String)
def getMaxIdFromTable( db, tableName, idField ):
    query = QtSql.QSqlQuery( db )
    query.prepare( "SELECT " + idField + " FROM " + tableName + " ORDER BY " + idField + " DESC LIMIT 1;" )
    query.exec_()

    if query.isActive():
        if query.first():
            return int( str ( query.value(0).toString() ))
        else:
            return 0

        query.finish()
    else:
        showQueryError(query)
        query.finish()
        return -9999

def showQueryError(query):
    QtGui.QMessageBox.warning( None, "Database Error", \
        QtCore.QString( "%1 \n %2" ).arg( query.lastError().text()).arg( query.lastQuery() ) )
