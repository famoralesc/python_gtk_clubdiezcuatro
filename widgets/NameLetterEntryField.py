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
# Ricardo Mendez L. rmendezlorca@gmail.com
import gtk
import gobject
import pygtk
import locale
import time, datetime
import string
from CustomEntryField import CustomEntryField

class NameLetterEntryField(CustomEntryField):
    def __init__(self, str1=None, str2=None, int1=50, int2=None):
        CustomEntryField.__init__(self)
        self.letterKeys=('a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M','n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z','space','.')
        self._lunghezza = int1
        if self._lunghezza > 0:
            self.set_max_length(self._lunghezza)
            self.set_width_chars(self._lunghezza)
        self.acceptedKeys = self.controlKeys +  self.letterKeys
        self.connect('changed', self.on_change)
##        self.connect('activate',self.activate)

    def do_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname not in self.acceptedKeys:
            return True
        data = widget.get_text()
        if (len(data) >= self._lunghezza) and (keyname not in self.controlKeys):
            return True
        widget.set_text(data.upper())   
    def on_change(self, widget):
        widget.set_position(-1)
