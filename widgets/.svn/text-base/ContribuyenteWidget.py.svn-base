# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import gtk
import gobject
import pygtk
import RUTEntryField
class ContribuyenteWidget(gtk.HBox):

    __gsignals__ = {'toggled' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_OBJECT, (gobject.TYPE_OBJECT, ) )}

    def __init__(self, str1="",str2="",int1=5,int2=None):
        self.estado = int1
        self.txtRut = RUTEntryField.RUTEntryField()
        self.txtNombre = gtk.Entry()
        self.txtApellidoP = gtk.Entry()
        self.txtApellidoM = gtk.Entry()
        gtk.HBox.__init__(self, False, 0)
        self.pack_start(self.txtRut)
        self.pack_start(self.txtNombre)
        self.pack_start(self.txtApellidoP)
        self.pack_start(self.txtApellidoM)
        
        self.txtRut.connect('key-press-event', self.txtRutKeyPress,self.txtRut)
        self.txtNombre.connect('key-press-event', self.txtNombreKeyPress,self.txtNombre)
        self.txtApellidoP.connect('key-press-event', self.txtApellidoPKeyPress,self.txtApellidoP)
        self.txtApellidoM.connect('key-press-event', self.txtApellidoMKeyPress,self.txtApellidoM)
        self.connect("show", self.on_show)

    def txtRutKeyPress(self, widget,*args):
        print "rut_keypress"
        if len(widget.get_text()) > 1:
            if int(widget.get_text()[:2]) >= 50:
                self.txtApellidoM.hide()
                self.txtApellidoP.hide()
            else:
                self.txtApellidoM.show()
                self.txtApellidoP.show()
    def txtNombreKeyPress(self, widget,*args):
        print "Nombre"
    def txtApellidoPKeyPress(self, widget,*args):
        print "Apellido Paterno"
    def txtApellidoMKeyPress(self, widget,*args):
        print "Apellido Materno"
    def do_toggled(self,*rb):
        if type(rb[0])== gtk.RadioButton:
            self.estado = int(rb[0].get_name())
            print self.estado
            self.emit('toggled',self)
    def setRut(self,rut = ''):
        self.txtRut.set_text(rut)
    def getRut(self):
        return self.txtRut.get_text()
    def setCustomLabel(self, id=None, labelText='', buttonText='', container=None):
        self._id = id
        self.label.set_text(self._labelText + labelText)
        self.buttonLabel.set_text(self._buttonText + buttonText)
        self._container = container


    def getContainer(self):
        return self._container


    def setContainer(self, container=None):
        self._container = container


    def on_show(self, event):
        (width, heigth) = self.get_size_request()
        if width == -1:
            self.setSize()


    def setSize(self, size=None):
        if size is None:
            size = -1
            parent = self.get_parent()
            if parent is not None:
                if parent.__class__ is gtk.Alignment:
                    (width, heigth) = parent.get_size_request()
                    size = width

        self.set_size_request(size, -1)


#gobject.type_register(CustomLabel)
