# -*- coding: utf-8 -*-

import asyncio
import pyperclip
from PyQt5 import QtCore, QtGui, QtWidgets
from sources.geniusv2 import *
from qasync import QEventLoop, asyncSlot
import sys


class Ui_dialog(object):
    def __init__(self):
        self.testo_lyrics = ""
        self.url = ""
        self.info = ""
        self.canzone = ""
        self.artista = ""
        

    def setupUi(self, dialog):
        dialog.setFixedSize(692, 773)

        dialog.setObjectName("dialog")
        dialog.resize(692, 762)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        dialog.setFont(font)
        dialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        dialog.setMouseTracking(True)
        dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        dialog.setAcceptDrops(False)
        dialog.setWindowIcon(QtGui.QIcon('spotifylogo.jpg'))
        dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint)
        dialog.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint)

        self.info_spotify = QtWidgets.QLabel(dialog)
        self.info_spotify.setGeometry(QtCore.QRect(10, 70, 671, 41))
        font = QtGui.QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.info_spotify.setFont(font)
        self.info_spotify.setAutoFillBackground(True)
        self.info_spotify.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.info_spotify.setFrameShadow(QtWidgets.QFrame.Plain)
        self.info_spotify.setObjectName("info_spotify")
        self.lyrics = QtWidgets.QTextBrowser(dialog)
        self.lyrics.setGeometry(QtCore.QRect(10, 120, 671, 591))
        self.lyrics.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.lyrics.setOpenExternalLinks(True)
        self.lyrics.setAcceptRichText(True)
        self.lyrics.setAutoFillBackground(True)
        self.lyrics.setObjectName("lyrics")
        self.refresh = QtWidgets.QPushButton(dialog)
        self.refresh.setGeometry(QtCore.QRect(10, 10, 131, 31))
        self.refresh.setObjectName("refresh")
        self.pushButton = QtWidgets.QPushButton(dialog)
        self.pushButton.setGeometry(QtCore.QRect(580, 720, 101, 41))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(10, 50, 101, 16))
        self.label.setObjectName("label")
        self.author = QtWidgets.QLabel(dialog)
        self.author.setObjectName(u"author")
        self.author.setGeometry(QtCore.QRect(630, 0, 101, 16))
        self.author.setOpenExternalLinks(True)

        self.link = QtWidgets.QLabel(dialog)
        self.link.setObjectName(u"link")
        self.link.setGeometry(QtCore.QRect(20, 720, 71, 21))
        self.link.setOpenExternalLinks(True)

        self.avviso = QtWidgets.QLabel(dialog)
        self.avviso.setObjectName(u"avviso")
        self.avviso.setGeometry(QtCore.QRect(20, 740, 271, 20))

    
        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        self.refresh.clicked.connect(lambda: self.cliccato())
        self.pushButton.clicked.connect(lambda: self.copia_lyrics())

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Spotify Lyrics by Ale :)"))
        self.lyrics.setHtml(_translate("dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI Semibold\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.refresh.setText(_translate("dialog", "Ricarica"))
        self.pushButton.setText(_translate("dialog", "Copia lyrics"))
        self.label.setText(_translate("dialog", "In riproduzione..."))
        self.author.setText(_translate("dialog", '<a>By </a><a href="https://github.com/aleeeee1">Ale</a>'))
        self.link.setText(_translate("dialog", "Link"))
        self.avviso.setText(_translate("dialog", "(se ci sono problemi con la lyrics, ricarica)"))

    
    
    @asyncSlot()
    async def cliccato(self):
        await self.main()
    def copia_lyrics(self):
        pyperclip.copy(self.testo_lyrics)


    async def aggiorna_info(self):
        canzone, artista = info_song()
        if artista == "Advertisement" or canzone == "Advertisement":
            url = "Link"
            testo = "Pubblicità"
            canzone, artista = "Pubblicità in corso", ""

        else:
            link = await cerca_link(canzone, artista)
            print(link)
            testo = await lyrics(link)

            url = f'<a href={link}>Link</a>'
            

        self.url = url
        self.testo_lyrics = testo
        self.canzone, self.artista = canzone, artista

    async def main(self):
        canzone, artista = info_song()
        self.info_spotify.setText(f"{canzone} - {artista}")

        self.lyrics.setText("Caricamento...")
        await self.aggiorna_info()
        self.info_spotify.setText(f"{self.canzone} - {self.artista}")
        self.lyrics.setText(self.testo_lyrics)
        self.link.setText(self.url)
        







if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    ui.cliccato()
    
    with loop:
        loop.run_forever()



