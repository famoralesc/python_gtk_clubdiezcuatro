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

class ClasificacionClienteWidget(gtk.HBox):

    __gsignals__ = {'toggled' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_OBJECT, (gobject.TYPE_OBJECT, ) )}

    def __init__(self, str1="",str2="",int1=5,int2=None):
        self.estado = int1
        self.r1 = gtk.RadioButton()
        self.r1.set_name(1)
        self.r2 = gtk.RadioButton(self.r1)
        self.r1.set_name(2)
        self.r3 = gtk.RadioButton(self.r1)
        self.r1.set_name(3)
        self.r4 = gtk.RadioButton(self.r1)
        self.r1.set_name(4)
        self.r5 = gtk.RadioButton(self.r1)
        self.r1.set_name(5)
        gtk.HBox.__init__(self, False, 0)
        self.pack_start(self.r1)
        self.pack_start(self.r2)
        self.pack_start(self.r3)
        self.pack_start(self.r4)
        self.pack_start(self.r5)
##        self.button = gtk.ToggleButton()
##        hbox = gtk.HBox(False, 3)
##        self.image = gtk.Image()
##        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'modifica16x16.png')
##        self.image.set_from_pixbuf(pbuf)
##        hbox.pack_start(self.image, False, False, 0)
##        self.buttonLabel = gtk.Label()
##        self.buttonLabel.set_text(self._buttonText)
##        hbox.pack_start(self.buttonLabel, False, False, 0)
##        self.button.add(hbox)
##
##        self.label = gtk.Label()
##        self.label.set_property('xalign',0)
##        self.label.set_text(self._labelText)
##        self.pack_start(self.button, False, False, 0)
##        self.pack_start(self.label, True, True, 5)
        self.r1.connect('toggled', self.do_toggled)
        self.r2.connect('toggled', self.do_toggled)
        self.r3.connect('toggled', self.do_toggled)
        self.r4.connect('toggled', self.do_toggled)
        self.r5.connect('toggled', self.do_toggled)
        self.connect("show", self.on_show)


    def do_button_clicked(self, button):
        self.emit('clicked', button)
    def do_toggled(self,rb):
        self.estado = int(rb.get_name())
        self.emit('toggled',self,)
    def setEstado(self,estado = 1):
        if estado ==1:
            self.r1.set_active(True)
        elif estado ==2:
            self.r2.set_active(True)
        elif estado ==3:
            self.r3.set_active(True)
        elif estado ==4:
            self.r4.set_active(True)
        elif estado ==5:
            self.r5.set_active(True)
        
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
