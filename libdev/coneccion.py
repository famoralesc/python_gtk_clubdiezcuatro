#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Clases para Widgets de conexiÃ³n en el sistema
#  (c) Fernando San MartÃ­n ín Woerner 2004
#  snmartin@galilea.cl

#Modulos que se requieren para esta clase

import sys
import gobject
import gtk
import time
from gtk import Dialog
import os
from types import StringType

from dialogos import dlgError
from sqlalchemy import orm, Table, MetaData
from orm.repository import Usuarios
#from coneccion_pg import connect
#import spg as psycopg
class dlgConeccion(Dialog):

    def __init__(self, window=None, db=None, rc=None,padre=None):

        lbl = unicode("Registro de Personal")
        Dialog.__init__(self, lbl.encode("utf-8"), window, 0,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))

        if padre!=None:
            self.padre=padre
        else:
            self.padre=None

        self.secciones = []
        self.coneccion = None
        self.ventana = window

        hbox = gtk.HBox(False, 8)
        hbox.set_border_width(8)
        self.vbox.pack_start(hbox, False, False, 0)
        stock = gtk.Image()
        stock.set_from_stock(gtk.STOCK_DIALOG_AUTHENTICATION, gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(stock, False, False, 0)
        table = gtk.Table(3, 2)
        table.set_row_spacings(4)
        table.set_col_spacings(4)
        hbox.pack_start(table, True, True, 0)

        self.txtUsuario = gtk.Entry()

        label = gtk.Label("Usuario")
        label.set_use_underline(True)
        table.attach(label, 0, 1, 1, 2)

        table.attach(self.txtUsuario, 1, 2, 1, 2)
        label.set_mnemonic_widget(self.txtUsuario)
        lbl = unicode("Contraseña")
        label = gtk.Label(lbl.encode("utf-8"))
        label.set_use_underline(True)
        table.attach(label, 0, 1, 2, 3)
        self.txtPassword = gtk.Entry()
        self.txtPassword.set_visibility(0)
        self.txtPassword.set_invisible_char(unicode("*","utf8"))
        self.txtPassword.set_text("")
        self.txtPassword.set_activates_default(1)
        table.attach(self.txtPassword, 1, 2, 2, 3)
        label.set_mnemonic_widget(self.txtPassword)
        self.set_default_response(gtk.RESPONSE_OK)
    
    def execute(self, cnx):
        self.show_all()
        self.txtUsuario.grab_focus()
        response = self.run()

        self.usuario = self.txtUsuario.get_text()
        self.password = self.txtPassword.get_text()

        if response == gtk.RESPONSE_OK:
            
            Session = orm.sessionmaker(cnx)
            session = Session()
            # TODO: encriptar la password y compararla encriptada
            usuario_verificado = session.query(Usuarios).filter_by(
                                                        username=self.usuario, 
                                                        password \
                                                        = self.password).\
                                                        first()
                                                        
            if usuario_verificado is not None:
                return usuario_verificado
            pass
#            except:
#                pass
            
        if response == gtk.RESPONSE_CANCEL:
            return 

    def get_active_text(self, combobox):
        model = combobox.get_model()
        active = combobox.get_active()

        if active < 0:
            self.coneccion = None
            return None

        for i in self.secciones:

            if model[active][0] == i[0]:

                self.txtUsuario.set_text(i[4])

        self.coneccion = model[active][0]

        return model[active][0]

class dlgSeleccionEmpresa(Dialog):

    def __init__(self, cnx=None, window=None):

        self.ventana = window
        self.cnx = cnx
        self.cod_empresa = None

        if cnx == None:
            dlgError(self.ventana, 'No hay una conexión activa.')
            return

        lbl = unicode("Selección de Empresa")
        Dialog.__init__(self, lbl.encode("utf-8"), window, 0,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        hbox = gtk.HBox(False, 8)
        hbox.set_border_width(8)
        self.vbox.pack_start(hbox, 1, False, 0)
        stock = gtk.Image()
        stock.set_from_stock(gtk.STOCK_HOME, gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(stock, False, False, 0)
        label = gtk.Label("Empresa")
        label.set_use_underline(True)
        hbox.pack_start(label, 0, 0, 0)

        try:
            r = cnx.cursor()
            r.execute("select text(cod_empresa), descripcion_empresa from cc.empresa order by descripcion_empresa")
            l = r.fetchall()

        except :
            dlgError(self.ventana, StringType(sys.exc_info()[1]))
            return 0

        self.modelo = gtk.ListStore(str, str)

        for i in l:
            self.modelo.append([i[0], unicode(i[1]).encode('utf-8')])


        self.combo = gtk.ComboBox(self.modelo)
        cell = gtk.CellRendererText()
        self.combo.pack_start(cell, True)
        self.combo.add_attribute(cell, 'text', 0)

        cell = gtk.CellRendererText()
        self.combo.pack_start(cell, True)
        self.combo.add_attribute(cell, 'text', 1)

        self.combo.set_active(0)
        self.cod_empresa = l[0][0]

        self.combo.set_size_request(300,25)

        hbox.pack_start(self.combo, True, True, 0)
        label.set_mnemonic_widget(self.combo)
        self.set_default_response(gtk.RESPONSE_OK)
        self.show_all()
#        self.combo.grab_focus()

    def execute(self):
        try:
            response = self.run()
    
            if response == gtk.RESPONSE_OK:
                self.cod_empresa = self.modelo[self.combo.get_active()][0]
                self.nom_empresa = self.modelo[self.combo.get_active()][1]
            elif response == gtk.RESPONSE_CANCEL:
                self.cod_empresa = None
                self.nom_empresa =None
        except:
            self.cod_empresa = None
            self.nom_empresa =None
