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
import locale
import time, datetime
import string
from CustomEntryField import CustomEntryField

class RUTEntryField(CustomEntryField):
# Effettua la validazione delle date

    def __init__(self, str1=None, str2=None, int1=None, int2=None):
        CustomEntryField.__init__(self)

        self._lunghezza = 12
        self.set_width_chars(12)
        self.acceptedKeys = self.controlKeys + self.numberKeys + ('k','K')
        self.connect('changed', self.on_change)


    def do_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname not in self.acceptedKeys:
            gtk.gdk.beep()
            return True
        data = widget.get_text()
        if (len(data) >= self._lunghezza) and (keyname not in self.controlKeys) and len(widget.get_selection_bounds())==0:
            gtk.gdk.beep()
            return True
        if (keyname not in self.controlKeys):
            #if (len(data) in (2,6)):
            #    data = data + "."
            #elif len(data) ==10:
            #    data = data + "-"
            widget.set_text(data)


    def do_focus_out_event(self, widget, event):
        if widget.get_text() != '':
            widget.set_text(self.parse_rut(widget.get_text()))
            if not self.valida_rut(widget.get_text()):
                gtk.gdk.beep()
                widget.grab_focus()
                return False
            else:
                return False
        else:
            gtk.gdk.beep()
            return False
    def do_activate_event(self, widget, event):
        if widget.get_text() != '':
            widget.set_text(self.parse_rut(widget.get_text()))
            if not self.valida_rut(widget.get_text()):
                gtk.gdk.beep()
                widget.grab_focus()
                return False
            else:
                return False
        else:
            gtk.gdk.beep()
            return False
    def parse_rut(self,rut):
        if rut == "":
            return rut
        rut = string.replace(rut,".","").replace("-","")
        rut = "0000000000"+ rut
        l = len(rut)
        rut_aux = "-" + rut[l-1:l]
        l = l-1
        while 2 < l:
            rut_aux = "."+ rut[l-3:l] +rut_aux
            l = l-3
        rut_aux = rut[0:l] +rut_aux
        l = len(rut_aux)
        rut_aux = rut_aux[l-12:l]
        return rut_aux
    def valida_rut(self,rut=None):
        if not rut: return 0
        es_rut = False
        cadena = "234567234567"
        dig_rut = rut[-1]
        rut = rut.replace(".", "")
        rut = rut[:rut.find("-")]
        rut = rut.replace(" ", '0')
        j, suma, i = 0, 0, len(rut) -1
        while i >= 0:
                try:
                        suma = suma + (int(rut[i]) * int(cadena[j]))
                except:
                        return 0
                i = i - 1
                j = j + 1
        divid = int(suma/11)
        mult = int(divid*11)
        dife = suma - mult
        digito = 11 - dife
        if digito == 10:
                caract = "K"
        elif digito == 11:
                caract = "0"
        else:
                caract = str(digito).replace(" ", "")
        if caract == dig_rut: 
                es_rut = True
        return es_rut
    
    def on_change(self, widget):
        widget.set_position(-1)


    def setNow(self):
        data = datetime.datetime.now()
        s = string.zfill(str(data.day), 2) + '/' + string.zfill(str(data.month),2) + '/' + string.zfill(str(data.year),4)
        self.set_text(s)

#gobject.type_register(DateEntryField)
