# SimpleGladeApp.py
# Module that provides an object oriented abstraction to pygtk and libglade.
# Copyright (C) 2004 Sandino Flores Moreno

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import os
import sys
import gtk
import gtk.glade
import weakref
import inspect
try :
    from PrefixGladeApp import PrefixActions
except:
    print "no se importo PrefixActions"

def bindtextdomain(app_name, i18n_dir):
    try:
        import locale
        import gettext
        locale.setlocale(locale.LC_ALL, "")
        gtk.glade.bindtextdomain(app_name, i18n_dir)
        gettext.install(app_name, i18n_dir, unicode=1)
    except (IOError,locale.Error), e:
        print "Warning", app_name, e
        __builtins__.__dict__["_"] = lambda x : x

class SimpleGladeApp(dict):
    def __init__(self, glade_filename, main_widget_name=None, domain=None, **kwargs):
        if os.path.isfile(glade_filename):
            self.glade_path = glade_filename
        else:
            glade_dir = os.path.split( sys.argv[0] )[0]
            self.glade_path = os.path.join(glade_dir, glade_filename)
        for key, value in kwargs.items():
            try:
                setattr(self, key, weakref.proxy(value) )
            except TypeError:
                setattr(self, key, value)
        self.glade = None
        gtk.glade.set_custom_handler(self.custom_handler)
        self.glade = gtk.glade.XML(self.glade_path, main_widget_name, domain)
        if main_widget_name:
            self.main_widget = self.glade.get_widget(main_widget_name)
        else:
            self.main_widget = None
        self.add_callbacks(self)
        self.new()
        actions = PrefixActions(self.add_mandatory, self.set_error_status)
        self.prefix_actions = actions
        self.add_prefix_actions(actions)

    def set_error_status(self, widget, error_status):
        if error_status:
            color_s = "#FF6B6B"
            widget.set_data("is-valid", None)
        else:
            widget.set_data("is-valid", True)
            color_s = "#FFFFFF"
        color = gtk.gdk.color_parse(color_s)
        widget.modify_base(gtk.STATE_NORMAL, color)
        
        can_apply = True
        for mandatory in self.prefix_actions.mandatories:
            if not mandatory.get_data("is-valid"):
                can_apply = False
        try:
            self.btnGuardar.set_sensitive(can_apply)
        except:
            try:
                self.btnAceptar.set_sensitive(can_apply)
            except:
                self.btnAplicar.set_sensitive(can_apply)
            
    def add_mandatory(self, widget):
        try:
            self.prefix_actions.mandatories.append(widget)
            label_prefix = '<b><span color="red">*</span></b>'
            eid = widget.get_name()[ len("txt") : ]
            label = getattr(self,"lbl%s" % eid)
            markup = label_prefix + label.get_label()
            label.set_markup(markup)
        except:
            return
    def add_callbacks(self, callbacks_proxy):
        self.glade.signal_autoconnect(callbacks_proxy)
        
    def add_prefix_actions(self, prefix_actions_proxy):
        prefix_s = "prefix_"
        prefix_pos = len(prefix_s)
        
        is_method = lambda t : callable( t[1] )
        is_prefix_action = lambda t : t[0].startswith(prefix_s)
        drop_prefix = lambda (k,w): (k[prefix_pos:],w)
        
        members_t = inspect.getmembers(prefix_actions_proxy)
        methods_t = filter(is_method, members_t)
        prefix_actions_t = filter(is_prefix_action, methods_t)
        prefix_actions_d = dict( map(drop_prefix, prefix_actions_t) )
        
        for widget in self.glade.get_widget_prefix(""):
            widget_name = widget.get_name()
            prefixes_name_l = widget_name.split(":")
            prefixes = prefixes_name_l[ : -1]
            widget_api_name = prefixes_name_l[-1]
            widget.set_name(widget_api_name)
            self[widget_api_name] = widget
            if prefixes:
                widget.set_data("prefix", prefixes)
                for prefix in prefixes:
                    if prefix in prefix_actions_d:
                        prefix_action = prefix_actions_d[prefix]
                        prefix_action(widget)
                        
    def custom_handler(self,
            glade, function_name, widget_name,
            str1, str2, int1, int2):
        try:
            handler = getattr(self, function_name)
            return handler(str1, str2, int1, int2)
        except AttributeError:
            return None

    def __getattr__(self, name):
        if name in self:
            data = self[name]
            return data
        else:
            widget = self.glade.get_widget(name)
            if widget != None:
                self[name] = widget
                return widget
            else:
                raise AttributeError, name

    def __setattr__(self, name, value):
        self[name] = value

    def new(self):
        pass

    def on_keyboard_interrupt(self):
        pass

    def gtk_widget_show(self, widget, *args):
        widget.show()

    def gtk_widget_hide(self, widget, *args):
        widget.hide()

    def gtk_widget_grab_focus(self, widget, *args):
        widget.grab_focus()

    def gtk_widget_destroy(self, widget, *args):
        widget.destroy()

    def gtk_window_activate_default(self, widget, *args):
        widget.activate_default()

    def gtk_true(self, *args):
        return True

    def gtk_false(self, *args):
        return False

    def gtk_main_quit(self, *args):
        gtk.main_quit()

    def main(self):
        gtk.main()

    def quit(self):
        gtk.main_quit()

    def run(self):
        try:
            self.main()
        except KeyboardInterrupt:
            self.on_keyboard_interrupt()
