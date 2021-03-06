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

class CustomEntryField(gtk.Entry):
    #'Down','Tab',
    controlKeys = ('Down','Tab','Delete','KP_Delete','BackSpace','ISO_Left_Tab',
                   'Left','Right','Up',
                   'KP_Left','KP_Right','KP_Down','KP_Up',
                   'Home','End','KP_Home','KP_End', 'Return', 'KP_Enter',
                   'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12')
    delimiterKeys = ('comma', 'period', 'KP_Decimal')
    signKeys = ('minus','KP_Subtract','plus','KP_Add')
    numberKeys = ('0','1','2','3','4','5','6','7','8','9',
                  'KP_0','KP_1','KP_2','KP_3','KP_4','KP_5','KP_6','KP_7','KP_8','KP_9')
    dateKeys = ('slash', 'KP_Divide')
    dateTimeKeys = ('slash', 'KP_Divide', 'colon', 'space')
    dateChars = ('/', '-')
    dateTimeChars = ('/', '-', ':', ' ')

    def __init__(self):
        gtk.Entry.__init__(self)
        self.connect('key_press_event', self.do_key_press_event)
        self.connect('focus_out_event', self.do_focus_out_event)
        self.connect('paste_clipboard', self.do_paste_clipboard)
        self.connect("show", self.on_show)


    def do_key_press_event(self, widget, event):
        pass


    def do_focus_out_event(self, widget, event):
        pass


    def do_paste_clipboard(self, widget):
        self.emit_stop_by_name('paste_clipboard')

    
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


#gobject.type_register(CustomEntryField)
