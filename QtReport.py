# -*- coding: utf-8 -*-
"""
/***************************************************************************
QtReport
Reporting Utility for based on Qt's RichText
                             -------------------
begin                : 2011-05-26
copyright            : (C) 2011 by Bernhard Stroebl
email                : b.stroebl@stroweb.de
description: QtReport is a child of QPainter class. The text itself is
comtained in a QTextDocument. Adding Text to it can be done by either
QTextDocument's or QTextCursor's methods or (simpler) through QtReport's
own methods.
When printed to a printer a QtReport can accomodate
headers and footers (if defined for this instance of QtReport).
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


from PyQt4 import QtCore, QtGui

class QtReport(QtGui.QPainter):
    def __init__(self, device, iface, columns = 1):
        QtGui.QPainter.__init__(self, device)

        # reference to QgsInterface-instance
        self.iface = iface
        self.device = device

        # initialize private Attributes
        self.__doc = QtGui.QTextDocument()
        self.__cursor = QtGui.QTextCursor(self.__doc)
        self.__cursor.movePosition(QtGui.QTextCursor.Start)
        self.__header = None
        self.__headerRect = QtCore.QRect(QtCore.QPoint(0, 0), QtCore.QSize(0, 0))
        self.__footer = None
        self.__footerRect = QtCore.QRect(QtCore.QPoint(0, 0), QtCore.QSize(0, 0))
        self.__pageNumber = 1
        self.__isFirstBlock = True
        self.__pageNumbering = 0 #0 no 1 page numbers 2 "page x of y"
        self.__defaultUnit = QtGui.QPrinter.Point
        self.__reportTitleRect = QtCore.QRect()
        self.__currentSection = 0
        self.__currentSubSection = 0

        # initalize fonts
        self.setTextFont(QtGui.QFont("Arial", 10, QtGui.QFont.Normal))

        # initialize settings
        self.__setTextRect()
        self.setColumns(columns) # calls __setColumnRect
        self.__lastBottom = self.__columnRect.top()

    #++++++++++++++++++++++++++++++++++++++++
    # misc functions
    #++++++++++++++++++++++++++++++++++++++++

    def __toPhysical(self, value, unit = None):
        '''Converts a value given in units into a value in pysical units'''

        if not unit:
            unit = self.__defaultUnit

        pysicalHeight = self.device.paperRect().height()
        unitHeight = self.device.paperRect(unit).height()
        pysicalValue = (pysicalHeight * value) / unitHeight
        return pysicalValue

    def __debug(self, msg):
        QtGui.QMessageBox.information(None,"",msg)

    def __checkFont(self, font, defaultFont = None):
        '''Check a font's validity else return defaultFont'''

        if font:
            if not isinstance(font, QtGui.QFont):
                font = defaultFont
        else:
            font = defaultFont

        if not font:
            font = self.__defaultFont

        return font

    def __asFormat(self, font, defaultFont):

        format = QtGui.QTextCharFormat()
        format.setFont(font)
        return format

    def __checkColor(self, color, defaultColor):
        '''Check a color's validity else, return defaultColor or black'''

        if not defaultColor:
            defaultColor = QtGui.QColor(QtCore.Qt.black)

        if color:

            if not isinstance(color, QtGui.QColor):
                color = defaultColor
        else:
            color = defaultColor

        return color

    def __pageNumberHeight(self, addValue = 15):

        footerRect = self.boundingRect(self.__textRect, \
            QtCore.Qt.AlignRight, QtCore.QString("2"))
        return footerRect.height() + self.__toPhysical(addValue,QtGui.QPrinter.Point)

    def __footerHeight(self, addValue = 17):
        '''Calculate the height of the current footer'''

        if self.footer():
            return self.__footerRect.height() + \
                self.__toPhysical(addValue, QtGui.QPrinter.Point)
        elif self.__pageNumbering > 0:
            return self.__pageNumberHeight(addValue)
        else:
            return 0

    def __headerHeight(self, addValue = 10):
        '''Calculate the height of the current header'''

        if self.header():
            self.setFont(self.__headerFont)
            self.__headerRect = self.boundingRect(self.__textRect, \
                QtCore.Qt.AlignHCenter, self.__header)
            return headerRect.height() + self.__toPhysical(addValue, QtGui.QPrinter.Point)
        else:
            return 0

    def __isTitlePage(self):
        '''Checks if we are on the first page and a title has been added'''

        return (self.__pageNumber == 1 and not self.__reportTitleRect.isNull())



    #++++++++++++++++++++++++++++++++++++++++
    # getter functions
    #++++++++++++++++++++++++++++++++++++++++

    def textDocument(self):
        return self.__doc

    def cursor(self):
        return self.__cursor

    def header(self):
        return self.__header

    def footer(self):
        return self.__footer

    def pageNumbering(self):
        return self.__pageNumbering

    def userRect(self):
        '''Return the rect left on the current page'''

        return QtCore.QRect(self.__textRect.left(), \
                            self.__lastBottom, \
                            self.__textRect.width(), \
                            self.__textRect.height() - self.__lastBottom)

    #++++++++++++++++++++++++++++++++++++++++
    # setter functions
    #++++++++++++++++++++++++++++++++++++++++

    def setTextDocument(self, doc):
        self.__doc = doc

    def setHeader(self, header, font = None, penColor = None, bgColor = None):
        '''Set the header to header and enable headers'''

        viewport = self.viewport()

        if isinstance(header, str) or isinstance(header, QtCore.QString):

            if self.header() == None:
                oldHeight = 0
            else:
                # we already had a header defined
                oldHeight = self.__headerHeight()

            self.__headerFont = self.__checkFont(font, self.__headerFont)
            self.__headerPen = self.__checkColor(penColor, QtGui.QColor(QtCore.Qt.black))
            self.__headerBgColor = self.__checkColor(bgColor, QtGui.QColor(QtCore.Qt.white))
            self.__header = header
            newHeight = self.__headerHeight()
            self.__textRect.setTop(self.__textRect.top() - oldHeight + newHeight)

            if self.__isFirstBlock:
                self.__setColumnRect()
            else:
                self.pageBreak()
        else:
            raise InputError(text, "must be of class str or QString!")

    def setTextFont(self, font):
        '''Sets the text's default font'''

        if self.__isFirstBlock:
            font = self.__checkFont(font)
            self.__defaultFont = font
            fontSize = font.pointSize()

            self.__titleFont = QtGui.QFont("Arial", fontSize * 3.6, QtGui.QFont.Bold)
            self.__sectionFont = QtGui.QFont("Arial", fontSize * 2.4, QtGui.QFont.Bold)
            self.__subSectionFont = QtGui.QFont("Arial", fontSize * 1.6, QtGui.QFont.Bold)
            self.__headerFont = QtGui.QFont("Arial", fontSize, QtGui.QFont.Normal, True)
            self.__footerFont = QtGui.QFont("Arial", fontSize * 0.8, QtGui.QFont.Normal)

            if fontSize == -1:
                # font was defined in pixels
                fontSize = font.pixelSize()
                self.__titleFont.setPixelSize(fontSize * 3.6)
                self.__sectionFont.setPixelSize(fontSize * 2.4)
                self.__subSectionFont.setPixelSize(fontSize * 1.6)
                self.__headerFont.setPixelSize(fontSize)
                self.__footerFont.setPixelSize(fontSize * 0.8)

            # scale the other fonts according to the size
            # if we use a 10pt font title is 36pt, section 24pt etc.

            self.__setTextRect()


    def setFooter(self, footer, font = None):
        '''Set the footer to footer and calculates footerRect'''

        if isinstance(footer, str) or isinstance(footer, QtCore.QString):
            self.__footer = footer
            self.__footerFont = self.__checkFont(font, self.__footerFont)
            self.setFont(self.__footerFont)
            self.__footerRect = self.boundingRect(self.__textRect, \
                QtCore.Qt.AlignLeft, self.__footer)
        else:
            raise InputError(text, "must be of class str or QString!")

    def setPageNumbering(self, doIt = 1):
        '''Toggle page numbering'''

        if self.footer():
            # if there are footers we're done
            self.__pageNumbering = doIt
        else:

            if self.__pageNumbering != doIt:
                # setting has been toggled
                self.__pageNumbering = doIt
                pageNumberHeight = self.__pageNumberHeight()

                if self.__pageNumbering > 0:
                    self.__textRect.setBottom(self.__textRect.bottom() \
                        - pageNumberHeight)
                else:
                    self.__textRect.setBottom(self.__textRect.bottom() \
                        + pageNumberHeight)

                if not self.__isFirstBlock:
                    self.pageBreak()

    def setColumns(self, columns = 1):
        '''Enable or disable multicolumn mode'''

        if not isinstance(columns, int):
            columns = 1

        self.__numbColumns = columns

        if self.__isFirstBlock:
            self.__setColumnRect()
            self.__currentColumn = 1
        else:
            self.pageBreak()

    def setMargins(self, leftMargin, rightMargin, topMargin, bottomMargin, unit = QtGui.QPrinter.Point):
        '''Set the paper margins'''

        if not isinstance(unit, QtGui.QPrinter.Unit):
            unit = self.__defaultUnit

        leftMargin = self.__toPhysical(leftMargin, unit)
        rightMargin = self.__toPhysical(rightMargin, unit)
        topMargin = self.__toPhysical(topMargin, unit)
        bottomMargin = self.__toPhysical(bottomMargin, unit)
        viewport = self.viewport()
        viewport.setLeft(viewport.left() + leftMargin)
        viewport.setRight(viewport.right() - rightMargin)
        viewport.setTop(viewport.top() + topMargin)
        viewport.setBottom(viewport.bottom() - bottomMargin)
        self.setViewport(viewport)
        self.__setTextRect()

    def setUserRect(self, rect):
        '''Sets the rect left on the current page to rect'''

        if self.__numbColumns > 1:
            self.pageBreak()
        else:
            self.__lastBottom = rect.top()

    #++++++++++++++++++++++++++++++++++++++++
    # Private setter functions
    #++++++++++++++++++++++++++++++++++++++++

    def __setColumnRect(self):
        '''Set the rect where the user may append contents
        for one-column reports __columnRect is identical with __textRect'''

        if self.__numbColumns == 1:
            self.__columnRect = self.__textRect
        else:
            defaultFontMetrics = QtGui.QFontMetrics(self.__defaultFont, self.device)

            maxWidth = defaultFontMetrics.maxWidth()
            whiteSpace = self.__toPhysical(maxWidth)
            columnWidth = (self.__textRect.width() - \
                        ((self.__numbColumns - 1) * whiteSpace)) \
                        / self.__numbColumns
            topLeftX = self.__textRect.left() + \
                ((self.__currentColumn - 1) * (columnWidth + whiteSpace))

            if self.__isTitlePage():
                topLeftY = self.__titleBottom
                columnHeight = self.__textRect.height() - self.__titleBottom
            else:
                topLeftY = self.__textRect.top()
                columnHeight = self.__textRect.height()

            self.__columnRect = \
                QtCore.QRect(QtCore.QPoint(topLeftX, topLeftY), \
                             QtCore.QSize(columnWidth, columnHeight))

    def __setTextRect(self):
        '''Set the rect on the page where the user may append stuff'''

        self.__reportRect = self.viewport()
        self.__textSize = QtCore.QSizeF(self.__reportRect.width(),
                                        self.__reportRect.height() -
                                        self.__headerHeight() -
                                        self.__footerHeight())
        self.__doc.setPageSize(self.__textSize)
        self.__textRect = QtCore.QRect(QPoint(0, 0), self.__textSize.toSize())

    #++++++++++++++++++++++++++++++++++++++++
    # functions to draw stuff on the report.
    # Functions are named "print" so there is no mix up with Qt's draw-Functions
    #++++++++++++++++++++++++++++++++++++++++

    def __printFooter(self, position = - 1):
        '''Print the page footer'''

        if position == 1:
            align = QtCore.Qt.AlignRight
        else:
            align = QtCore.Qt.AlignLeft

        self.setFont(self.__footerFont)
        footerRect = self.boundingRect(self.viewport(), \
                                       align | QtCore.Qt.AlignBottom, \
                                       self.__footer)
        self.drawText(footerRect, align, self.__footer)

    def __printHeader(self, position = 0):
        '''Print the page header and draw a line underneath'''

        if position == -1:
            align = QtCore.Qt.AlignLeft
        elif position == 1:
            align = QtCore.Qt.AlignRight
        else:
            align = QtCore.Qt.AlignHCenter

        self.setFont(self.__headerFont)
        oldPen = self.pen()

        headerRect = self.boundingRect(self.viewport(), align, self.__header)
        bgBrush = QtGui.QBrush(self.__headerBgColor)

        self.fillRect(self.viewport().left(), \
                      self.viewport().top(), \
                      self.__textRect.width(), \
                      headerRect.height(), \
                      bgBrush)
        self.setPen(self.__headerPen)
        self.drawText(headerRect, align, self.__header)
        y = headerRect.bottom()
        y = y + self.__toPhysical(1)
        self.setPen(oldPen)
        line = QtCore.QLineF(self.__textRect.left(), y, self.__textRect.right(), y)
        self.drawLine(line)

    def __printPageNumber(self, position = 0):
        '''Print the page number'''

        if position == -1:
            align = QtCore.Qt.AlignLeft
        elif position == 1:
            align = QtCore.Qt.AlignRight
        else:
            align = QtCore.Qt.AlignHCenter

        self.setFont(self.__defaultFont)
        pageNumber = QtCore.QString(str(self.__pageNumber))
        pnRect = self.boundingRect(self.viewport(), align | QtCore.Qt.AlignBottom, \
                                   pageNumber)
        self.drawText(pnRect, align, pageNumber)

    def __printText(self, rect, text, font, \
                    flags = QtCore.Qt.AlignLeft | QtCore.Qt.TextWordWrap, \
                    color = QtCore.Qt.black):
        '''Draw text onto the report within rect
        using font, color and flags'''

        self.setFont(font)
        self.setPen(color)
        self.drawText(rect, flags, text.trimmed())
        self.__lastBottom = rect.bottom()
        self.__isFirstBlock = False

    def __printFrame(self):
        '''Print header, footer and page number'''

        pageNumberPosition = 0

        if not self.__isTitlePage():

            if self.header():
                self.__printHeader()

        if self.footer():
            self.__printFooter()
            pageNumberPosition = 1

        if self.__pageNumbering:
            self.__printPageNumber(pageNumberPosition)



    #++++++++++++++++++++++++++++++++++++++++
    # functions to append text to the report.
    #++++++++++++++++++++++++++++++++++++++++

    def __appendText(self, text, format, atCurrentPosition = False):
        '''Add any text to the end of the document'''

        if not atCurrentPosition:
            self.__cursor.movePosition(QtGui.QTextCursor.End)

        self.__cursor.insertBlock()
        self.__cursor.insertText(text, format)

    def appendHtml(self, html, atCurrentPosition = False):
        '''Add html-formatted text'''

        if not atCurrentPosition:
            self.__cursor.movePosition(QtGui.QTextCursor.End)

        self.__cursor.insertBlock()
        self.__cursor.insertHtml(html)

    def __appendSect(self, text, font):
        '''private method to append a section header'''

        thisFontMetrics = QtGui.QFontMetrics(font, self.device)
        thisLineSpacing = thisFontMetrics.lineSpacing()
        self.appendVSpace(thisLineSpacing * 1.5)
        format = self.__asFormat(font)
        self.appendTextBlock(text, format)
        self.appendVSpace(thisLineSpacing)

    def appendVSpace(self, space, unit = None, atCurrentPosition = False):
        '''Append a vertical space of height space in units'''

        if unit:

            if not isinstance(unit, QtGui.QPrinter.Unit):
                unit = None

        if unit:
            height = self.__toPhysical(space, unit)
        else:
            height = space

        format = QtGui.QTextCharFormat()
        format.setFontPointSize(height)
        self.__appendText("\n", format, atCurrentPosition)

    def appendTextBlock(self, text, font = None):
        '''Add a text in block layout'''

        if isinstance(text, str) or isinstance(text, QtCore.QString):
            font = self.__checkFont(font)
            format = self.__asFormat(font)
            self.__appendText(text, format)
        else:
            raise InputError(text, "must be of class str or QString!")

    def appendTitle(self, text, font = None):
        '''Add the Report Title if we are in the first TextBlock'''

        if isinstance(text, str) or isinstance(text, QtCore.QString):
            font = self.__checkFont(font, self.__titleFont)
            self.__cursor.movePosition(QtGui.QTextCursor.Start)
            self.appendVSpace(50, self.__defaultUnit, True)
            format = self.__asFormat(font)
            self.__appendText(text, format, True)
            self.appendVSpace(15, self.__defaultUnit, True)
        else:
            raise InputError(text, "must be of class str or QString!")

    def appendSection(self, text, font = None, numbered = False):

        if isinstance(text, str) or isinstance(text, QtCore.QString):
            font = self.__checkFont(font, self.__sectionFont)

            if numbered:
                self.__currentSection = self.__currentSection + 1
                text = str(self.__currentSection) + "  " + text

            self.__currentSubSection = 0 # reset
            self.__appendSect(text, font)
        else:
            raise InputError(text, "must be of class str or QString!")

    def appendSubSection(self, text, font = None, numbered = False):

        if isinstance(text, str) or isinstance(text, QtCore.QString):
            font = self.__checkFont(font, self.__subSectionFont)

            if numbered:
                self.__currentSubSection = self.__currentSubSection + 1
                text = str(self.__currentSection) + "." + str(self.__currentSubSection) + "  " + text

            self.__appendSect(text, font)
        else:
            raise InputError(text, "must be of class str or QString!")

    #++++++++++++++++++++++++++++++++++++++++
    # functions to append graphics to the report.
    #++++++++++++++++++++++++++++++++++++++++

    def appendMap(self):
        '''Print the current map to the report'''

        self.appendPixmap(self.iface.mapCanvas().canvasPixmap())

    def appendPixmap(self, pixmap, scaleToTextWidth = False, withFrame = True):
        '''Append a pixmap to the report'''

        tb = self.__columnRect.width()
        th = self.__columnRect.height()
        b = pixmap.width()

        decreaseWidth = (b > tb)
        increaseWidth = (b < tb and scaleToTextWidth)

        if increaseWidth:
            pixmapTb = pixmap.scaledToWidth(tb)

            if pixmapTb.height() < th:
                pixmap = pixmapTb

        if decreaseWidth:
            pixmap = pixmap.scaledToWidth(tb)

        h = pixmap.height()
        rh = th - self.__lastBottom

        if h > th:
            pixmap = pixmap.scaledToHeight(th)
            h = pixmap.height()

        if h > rh:
            self.columnBreak()

        self.drawPixmap(self.__columnRect.left(), \
                        self.__lastBottom,
                        pixmap)

        if withFrame:
            frameRect = QtCore.QRect(self.__columnRect.left(),
                                     self.__lastBottom,
                                     pixmap.width(),
                                     pixmap.height())
            self.drawRect(frameRect)

        self.__lastBottom = self.__lastBottom + pixmap.height()

    #++++++++++++++++++++++++++++++++++++++++
    # functions to structure the report.
    #++++++++++++++++++++++++++++++++++++++++

    def columnBreak(self):
        '''Function to enter a new column or a new page'''

        #self.__debug("columnBreak; currentColum = " + str(self.__currentColumn))

        if self.__currentColumn == self.__numbColumns:
            self.pageBreak()
        else:
            self.__currentColumn = self.__currentColumn + 1
            self.__setColumnRect()
            self.__lastBottom = self.__columnRect.top()

    def pageBreak(self):

        if self.__pageNumber == 1:
            self.__printFrame()

        self.__pageNumber = self.__pageNumber + 1
        self.__currentColumn = 1
        self.__setColumnRect()
        self.device.newPage()
        self.__printFrame()
        self.__lastBottom = self.__columnRect.top()


    def finish(self):

        if self.__pageNumber == 1:
            self.__pageNumbering = False
            self.__printFrame()

        self.end()



# Error classes
class Error(Exception):
    '''Base class for exceptions in this module.'''

    pass

class InputError(Error):
    '''Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    '''

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


import os.path, sys, tempfile, subprocess


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

