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

class CodProdEntryField(CustomEntryField):
# Effettua la validazione delle date

    def __init__(self, str1=None, str2=None, int1=None, int2=None):
        CustomEntryField.__init__(self)

        self._lunghezza = 20
        self.set_width_chars(20)
        self.consulta =('c','C','e','E','minus')
        self.multiplo =('*','KP_Multiply','Multi_key','asterisk')
        self.acceptedKeys = self.controlKeys + self.numberKeys + self.consulta+ self.multiplo
        self.connect('changed', self.on_change)


    def do_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname not in self.acceptedKeys:
            #print keyname
            gtk.gdk.beep()
            return True
        data = widget.get_text()
        if (len(data) >= self._lunghezza) and (keyname not in self.controlKeys):
            gtk.gdk.beep()
            return True
        if (keyname not in self.controlKeys):
            if (keyname in self.consulta)  and len(data) > 0:
                gtk.gdk.beep()
                return True
            if (keyname in self.multiplo)  and (len(data) == 0 or data.count("*") > 2 or True in [i in data for i in self.consulta]):
                gtk.gdk.beep()
                return True
##            if (len(data) in (2,6)):
##                data = data + "."
##            elif len(data) ==10:
##                data = data + "-"
##            widget.set_text(data)


    def do_focus_out_event(self, widget, event):
        return False
        data=widget.get_text()
        for c in self.dateChars:
            if c in data:
                data = data.replace(c, '')
        try:
            time.strptime(data, "%d%m%Y")
        except Exception:
            widget.set_text(self.parse_date(widget.get_text()))

    def parse_date(self,text):
        text=text.replace("/","-")
        (cY,cm,cd) = time.localtime()[0:3]
        try:
            (d,) = time.strptime(text, "%d")[2:3]
            m,Y = cm,cY
        except ValueError:
            try:    
                (m,d) = time.strptime(text, "%d-%m")[1:3]
                Y = cY
            except:
                (Y,m,d) = time.strptime(text, "%d-%m-%Y")[0:3]
                
        return "%02d/%02d/%d" % (d,m,Y)
    def on_change(self, widget):
        widget.set_position(-1)


    def setNow(self):
        data = datetime.datetime.now()
        s = string.zfill(str(data.day), 2) + '/' + string.zfill(str(data.month),2) + '/' + string.zfill(str(data.year),4)
        self.set_text(s)

#gobject.type_register(DateEntryField)
