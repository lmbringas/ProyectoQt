#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys , re
import time
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.uic import *
from PyQt4.QtWebKit import QWebView , QWebSettings
from PyQt4.QtNetwork import *
from PyQt4.QtGui import *
from PyQt4.QtCore import * 

class navigator(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(navigator,self).__init__(parent)
        self.ui=loadUi("buscadorr.ui",self)
        self.centrar()
        self.variables()
        self.userAgent()
        self.atributo()        
        self.ui.pu4_2.hide()
        self.ui.segLink.hide()
        self.show()
        self.conects()
        self.histo=False
        
#---------------------------------------------------------------------------
    
    def variables(self):
        self.vecWeb=[]
        self.vecLargo=[]
        self.vecTodo=[]
        self.centrar()
        self.contador=-1
        self.flag=0
        
    def centrar(self):
        pantalla = QtGui.QDesktopWidget().screenGeometry()
        tamano=  self.geometry()
        self.move((pantalla.width()-tamano.width())/2, (pantalla.height()-tamano.height())/2)

    def userAgent(self):
        self.web=QWebView(self)
        self.webbb_2.addWidget(self.web)
        self.useragent ='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36'
        self.request = QNetworkRequest()
        self.request.setRawHeader("User-Agent",self.useragent)
        self.web.page().userAgentForUrl = self.customuseragent
        self.request.setUrl(QtCore.QUrl('http://www.google.com.ar'))
        self.web.load(self.request)
    
    def conects(self):
        self.ui.actionSin_Historial.setCheckable(True)
        self.ui.actionSin_Historial.triggered.connect(self.sinHitorial)
        self.connect(self.web, QtCore.SIGNAL("loadProgress(int)"), self.empe)
        self.connect(self.web, QtCore.SIGNAL("loadFinished(bool)"), self.urldepag)
        self.ui.actionNueva_Pesta_a.triggered.connect(self.nuevaPestana)
        self.ui.actionNuevaVentana.triggered.connect(self.nuevaVentana)
        self.ui.actionSalir.triggered.connect(QtGui.qApp.quit)
        self.ui.actionHistorial.triggered.connect(self.historial)
        self.ui.actionAyuda.triggered.connect(self.estoEsUnaNegrada)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

    def atributo(self):
        self.ui.web.settings().setAttribute(QWebSettings.PluginsEnabled,True)
        self.tabWidget.setTabsClosable(True)
        self.ui.web.page().setForwardUnsupportedContent(True)
        self.ui.web.settings().setAttribute(QWebSettings.JavascriptEnabled,True)
        self.ui.web.settings().setAttribute(QWebSettings.JavascriptCanOpenWindows, True);
    def customuseragent():
        print 'called for %s' % url
        return 'custom ua'

#---------------------------------------------------------------------------
    def comprobacion(self):
        if  (self.ui.tabWidget.currentIndex() == 0):
        
            if self.flag==1:
                return self.vecWeb[self.tabWidget.currentIndex()]
            return self.web
        
        else:
            return self.vecWeb[self.tabWidget.currentIndex()-1]
    
    def busDina(self):
        self.ui.segLink.clear()
        texto=str(self.ui.lineEdit_3.text())
        with open('.historia.txt','r') as f:
            for x in f:
                self.ui.segLink.show()
                x=x.split(',')
                if texto in x[0]:
                    self.ui.segLink.addItem(x[0])
                    if  texto == '':
                        self.segLink.hide()
                    break
                else:
                    self.segLink.hide()
    
    def encontrado(self):
        self.encon=str(self.segLink.currentItem().text())
        self.cargar(self.encon)
    
    def buscar(self):
        self.tex = self.lineEdit_3.text()
        pat = re.compile('(.+)\\.(.+)')
        Http = re.compile('^http://')
        if pat.match(self.tex) and not Http.match(self.tex):
            self.url = 'http://' + self.tex
        elif not pat.match(self.tex):
            self.url = self.link(self.tex)
        self.cargar(self.url)

    def link(self,url):
        self.com={'Google':'https://www.google.com.ar/#q=',"Wikipedia":'http://es.wikipedia.org/wiki/',"Youtube":'https://www.youtube.com/results?search_query=','Traducir al Ingles':'https://translate.google.com.ar/#es/en/',"Traducir al Espanol":'https://translate.google.com.ar/#en/es/','Bing':'http://www.bing.com/search?q=','DuckDuckGo':'https://duckduckgo.com/?q=','Amazon':'http://www.amazon.com/s?ie=UTF8&field-keywords=','Diccionario RAE':'http://buscon.rae.es/drae/?type=3&val='}
        self.cb=str(self.ui.cbweb_2.currentText())
        self.comp=self.com[self.cb]

        if self.comp=='https://translate.google.com.ar/#en/es' or self.comp=='https://translate.google.com.ar/#es/en/' or 'http://buscon.rae.es/drae/?type=3&val=':
            self.url=self.comp+self.tex

        elif self.comp=='http://es.wikipedia.org/wiki/':
            self.url=self.comp+self.tex.replace(' ','_')

        else:
            self.url=self.comp+self.tex.replace(' ','+')
        return self.url

    def ok(self):   
        self.tex=str(self.ui.lineEdit_4.text())
        self.nose=self.link(self.tex)
        self.cargar(self.nose)

#---------------------------------------------------------------------------
    def estoEsUnaNegrada(self):
        self.pesConHisto('Ayuda.html')
    
    def sinHitorial(self):
        if self.histo==True:
            self.histo=False
        
        else:
            self.histo=True
       

    def cargar(self,url):
        self.comprobacion().setUrl(QtCore.QUrl(url))
    
    def atras(self):
        self.comprobacion().back()

    def ade(self):
        self.comprobacion().forward()

    def empe(self):
        self.segLink.hide()
        self.pu4_2.hide()
        self.pu3_2.show()

    def urldepag(self):
        if self.histo==True:
            pass
        
        else:
            hora=time.strftime('%X')
            fecha=time.strftime('%x')
            
            self.lineEdit_3.setText(self.comprobacion().url().toString())
            with open('.historia.txt','a+r') as f:
                f.write(str(self.comprobacion().url().toString()+','+hora+','+fecha+'\n'))
            
            self.pu3_2.hide()
            self.pu4_2.show()
            self.segLink.hide()
            self.ui.tabWidget.setTabText(self.tabWidget.currentIndex(),self.comprobacion().title())
            self.ui.setWindowTitle(self.comprobacion().title()+' - '+'EcheUau')

    def recar(self):
        self.comprobacion().reload()
 
    def stop(self):
        self.comprobacion().stop()
    
    def historial(self):
        a=history(self)
            
    def camText(self):
        self.lineEdit_3.setText(self.comprobacion().url().toString())
        self.segLink.hide()
    
    def closeTab(self,index):
        self.ui.tabWidget.removeTab(index)
        if  (self.ui.tabWidget.count() == 0):
            sys.exit()
        
        elif self.ui.tabWidget.currentIndex()==0:
            self.flag=1

        else:
            self.contador-=1
            self.vecWeb.pop()

    def nuevaPestana(self):
        self.contador+=1
        self.vecWeb.append(QWebView(self))
        self.ui.tabWidget.addTab(self.vecWeb[self.contador],self.comprobacion().title())
        self.ui.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
        self.cargar('http://www.google.com.ar/')
        self.connect(self.vecWeb[self.ui.tabWidget.currentIndex()-1], QtCore.SIGNAL("loadProgress(int)"), self.empe)
        self.connect(self.vecWeb[self.ui.tabWidget.currentIndex()-1], QtCore.SIGNAL("loadFinished(bool)"), self.urldepag)
        self.vecWeb[self.ui.tabWidget.currentIndex()-1].settings().setAttribute(QWebSettings.PluginsEnabled,True)
    
    def pesConHisto(self,unacosa):
        self.contador+=1
        self.vecWeb.append(QWebView(self))
        self.ui.tabWidget.addTab(self.vecWeb[self.contador],'Navigator')
        self.ui.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
        self.connect(self.vecWeb[self.ui.tabWidget.currentIndex()-1], QtCore.SIGNAL("loadProgress(int)"), self.empe)
        self.connect(self.vecWeb[self.ui.tabWidget.currentIndex()-1], QtCore.SIGNAL("loadFinished(bool)"), self.urldepag)
        self.vecWeb[self.ui.tabWidget.currentIndex()-1].settings().setAttribute(QWebSettings.PluginsEnabled,True)
        self.comprobacion().setUrl(QtCore.QUrl(unacosa))

    def nuevaVentana(self):
        navigator()

#---------------------------------------------------------------------------

class history(QtGui.QMainWindow):
    def __init__(self,navegadorActal=None, parent=None):
        super(history,self).__init__(parent)
        self.uil=loadUi("historial.ui",self)
        self.lista()
        self.show()
        self.nav = navegadorActal 

    def lista(self):
        with open('.historia.txt','r') as f:
            for x in f:
                x=x.split(',')
                self.uil.listwidget.addItem(x[0])
        
    
    def cambiar(self):
        self.uil.listwidget.clear()
        foo=self.uil.cmbox.currentText()
        if foo=='Url':
            with open('.historia.txt','r') as f:
                for x in f:
                    x=x.split(',')
                    self.uil.listwidget.addItem(x[0])
        else:
            with open('.historia.txt','r') as f:
                for x in f:
                    x=x.replace(',',' | ')
                    self.uil.listwidget.addItem(x)
    
    def elecion(self):
        elec=self.cmbox.currentText()
        lqbus=str(self.uil.ledit.text())
        self.uil.listwidget.clear()
        if lqbus=='':
            self.lista()
        
        if elec=='Url':
            with open('.historia.txt','r') as f:
                for x in f:    
                    if lqbus in x:
                        x=x.split(',')
                        self.uil.listwidget.addItem(x[0])         
        else:
             with open('.historia.txt','r') as f:
                for x in f:    
                    if lqbus in x:
                        x=x.split(',')
                        self.uil.listwidget.addItem(x[1]+' | '+x[2]+' | '+x[0])
             if lqbus=='':
                self.cambiar()
    
    def pasar(self):
        self.url=str(self.uil.listwidget.currentItem().text())
        self.url=self.url.split('|')
        self.nav.pesConHisto(self.url[0])
        
if __name__=="__main__":
	app=QtGui.QApplication(sys.argv)
	myapp = navigator()
	myapp.show()
	sys.exit(app.exec_())
