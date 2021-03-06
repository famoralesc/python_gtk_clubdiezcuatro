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
from CustomEntryField import CustomEntryField

class UnsignedIntegerEntryField(CustomEntryField):
# Effettua la validazione per interi senza segno

    def __init__(self, str1="", str2=None, int1=8, int2=None):
        CustomEntryField.__init__(self)

        self._lunghezza = int1
        self._default = str1
        if self._lunghezza > 0:
            self.set_max_length(self._lunghezza)
            self.set_width_chars(self._lunghezza)
        self.acceptedKeys = self.controlKeys + self.numberKeys


    def do_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname not in self.acceptedKeys:
            return True


    def do_focus_out_event(self, widget, event):
        try:
            if self.get_text()=='':
                return
            i = int(self.get_text())
            if self._lunghezza > 0:
                f = "%0" + str(self._lunghezza) + "d"
                self.set_text(f % i)
            else:
                self.set_text(str(i))
        except Exception:
            if self._default is None:
                i = 0
                self.set_text('')
            elif self._default == "<blank>":
                # empty
                self.set_text('')
            else:
                self.set_text(self._default)
        self.set_text(self.get_text().strip())

#gobject.type_register(UnsignedIntegerEntryField)
