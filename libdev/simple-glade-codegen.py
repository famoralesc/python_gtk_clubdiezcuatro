#!/usr/bin/env python

# simple-glade-codegen.py
# A code generator that uses pygtk, glade and SimpleGladeApp.py
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

import sys, os, re, codecs
import tokenize, shutil, time
import xml.sax
from xml.sax._exceptions import SAXParseException

header_format = """\
#!/usr/bin/env python
# -*- coding: UTF8 -*-

# Python module %(module)s.py
# Autogenerated from %(glade)s
# Generated on %(date)s
# Copyright (C) 2007 Victor Benitez
# Warning: Do not delete or modify comments related to context
# They are required to keep user's code

from package import *
from schema import class_%(_class)s
glade_dir = "Glade"


# Put your modules and data here

# From here through main() codegen inserts/updates a class for
# every top-level widget in the .glade file.

"""

class_format_frm = """\
class %(class)s(SimpleGladeApp):
%(t)sdef __init__(self,cnx =None, padre =None, glade_path="%(glade)s", root="%(root)s", domain=None):
%(t)s%(t)sglade_path = os.path.join(glade_dir, glade_path)
%(t)s%(t)sSimpleGladeApp.__init__(self, glade_path, root, domain)
%(t)s%(t)sif padre == None:
%(t)s%(t)s%(t)sself.padre = self
%(t)s%(t)s%(t)sself.ventana = self.%(root)s
%(t)s%(t)s%(t)sself.%(root)s.maximize()
%(t)s%(t)s%(t)sself.%(root)s.show()
%(t)s%(t)selse:
%(t)s%(t)s%(t)sself.padre = padre
%(t)s%(t)s%(t)sself.ventana = padre.ventana

%(t)sdef new(self):
%(t)s%(t)s#context %(class)s.new {
%(t)s%(t)sself.data=class_%(_class)s()
%(t)s%(t)s#self.data.set_en_uso(True)
%(t)s%(t)sself.crea_modelo()
%(t)s%(t)sself.crea_columnas()
%(t)s%(t)sself.carga_datos()
%(t)s%(t)s#context %(class)s.new }

%(t)s#context %(class)s custom methods {
%(t)s#--- Write your own methods here ---#
%(t)sdef crea_columnas(self):
%(t)s%(t)s'''Crea las columnas del gtk.TreeView 
%(t)s%(t)s'''
%(t)s%(t)scolumnas = []
%(t)s%(t)scolumnas.append([0,"Cod ","str"])
%(t)s%(t)scolumnas.append([1,"Desc","str"])

%(t)s%(t)sSimpleTree.GenColsByModel(self.modelo, columnas, self.tree)
%(t)sdef crea_modelo(self):
%(t)s%(t)s'''Crea un modelo basado en gtk.ListStore, en el cual carga
%(t)s%(t)slos datos de la tabla cliente de la base de datos local.
%(t)s%(t)s'''
%(t)s%(t)sself.modelo = gtk.ListStore(str, str)

%(t)sdef carga_datos(self):
%(t)s%(t)sself.modelo.clear()
%(t)s%(t)sfor i in self.data.select_criterial(self.data):
%(t)s%(t)s%(t)sself.modelo.append((i.get_cod_%(_class)s(),i.get_desc_%(_class)s()))

%(t)s#context %(class)s custom methods }

"""

class_format_dlg = """\
class %(class)s(SimpleGladeApp):
%(t)sdef __init__(self,cnx =None, padre =None, glade_path="%(glade)s", root="%(root)s", domain=None):
%(t)s%(t)sglade_path = os.path.join(glade_dir, glade_path)
%(t)s%(t)sSimpleGladeApp.__init__(self, glade_path, root, domain)
%(t)s%(t)sif padre == None:
%(t)s%(t)s%(t)sself.padre = self
%(t)s%(t)s%(t)sself.ventana = self.%(root)s
%(t)s%(t)s%(t)sself.%(root)s.maximize()
%(t)s%(t)s%(t)sself.%(root)s.show()
%(t)s%(t)selse:
%(t)s%(t)s%(t)sself.padre = padre
%(t)s%(t)s%(t)sself.ventana = padre.ventana
%(t)s%(t)sself.data=class_%(_class)s()


%(t)sdef new(self):
%(t)s%(t)s#context %(class)s.new {
%(t)s%(t)spass
%(t)s%(t)s#context %(class)s.new }

%(t)s#context %(class)s custom methods {
%(t)s#--- Write your own methods here ---#

%(t)sdef set_data(self,data):
%(t)s%(t)sself.data = data

%(t)sdef get_data(self):
%(t)s%(t)sreturn self.data
%(t)sdef aceptar(self):
%(t)s%(t)sself.data.set_desc_%(_class)s(self.txtDesc***.get_text())
%(t)s%(t)sself.data.save()

%(t)s#context %(class)s custom methods }

"""


callback_format = """\
%(t)sdef %(handler)s(self, widget, *args):
%(t)s%(t)s#context %(class)s.%(handler)s {
%(t)s%(t)spass
%(t)s%(t)s#context %(class)s.%(handler)s  %(widget)s}

"""

callback_format_btnCerrar = """\
%(t)sdef %(handler)s(self, widget, *args):
%(t)s%(t)s#context %(class)s.%(handler)s {
%(t)s%(t)sif self.ventana == self.%(root)s:
%(t)s%(t)s%(t)sself.quit()
%(t)s%(t)selse:
%(t)s%(t)s%(t)sdel self.padre.wins[self.etiqueta]
%(t)s%(t)s%(t)sself.padre.ntbPrincipal.remove_page(self.padre.ntbPrincipal.get_current_page())
%(t)s%(t)s%(t)sreturn 1
%(t)s%(t)s#context %(class)s.%(handler)s  %(widget)s}

"""

callback_format_Anadir = """\
%(t)sdef %(handler)s(self, widget, *args):
%(t)s%(t)s#context %(class)s.%(handler)s {
%(t)s%(t)sd=Dlg%(_class)s(None,self.padre)


%(t)s%(t)sif d.dlg_%(_class)s.run() == gtk.RESPONSE_OK:
%(t)s%(t)s%(t)sself.carga_datos()
%(t)s%(t)s%(t)sprint('aceptar')
%(t)s%(t)sd.dlg_%(_class)s.destroy()
%(t)s%(t)s#context %(class)s.%(handler)s  %(widget)s}

"""
callback_format_Quitar = """\
%(t)sdef %(handler)s(self, widget, *args):
%(t)s%(t)s#context %(class)s.%(handler)s {
%(t)s%(t)smodel,iter = self.tree.get_selection().get_selected()
%(t)s%(t)sif iter != None:
%(t)s%(t)s%(t)saux = class_%(_class)s()
%(t)s%(t)s%(t)saux.set_cod_%(_class)s(model.get_value(iter,0))
%(t)s%(t)s%(t)saux = aux.get()
%(t)s%(t)s%(t)saux.delete()
%(t)s%(t)s%(t)sself.carga_datos()
%(t)s%(t)s#context %(class)s.%(handler)s  %(widget)s}

"""

callback_format_Propiedades = """\
%(t)sdef %(handler)s(self, widget, *args):
%(t)s%(t)s#context %(class)s.%(handler)s {
%(t)s%(t)smodel,iter = self.tree.get_selection().get_selected()
%(t)s%(t)sif iter != None:
%(t)s%(t)s%(t)sd=Dlg%(_class)s(None,self.padre)
%(t)s%(t)s%(t)sd.get_data().set_cod_banco(model.get_value(iter,0))
%(t)s%(t)s%(t)sd.set_data(d.get_data().get())
%(t)s%(t)s%(t)sd.txtCod***.set_text(model.get_value(iter,0))
%(t)s%(t)s%(t)sd.txtDesc***.set_text(model.get_value(iter,1))
%(t)s%(t)s%(t)sif d.dlg_%(_class)s.run() == gtk.RESPONSE_OK:
%(t)s%(t)s%(t)s%(t)sself.carga_datos()
%(t)s%(t)s%(t)s%(t)sprint('aceptar')
%(t)s%(t)s%(t)sd.dlg_%(_class)s.destroy()
%(t)s%(t)s#context %(class)s.%(handler)s  %(widget)s}

"""

creation_format = """\
%(t)sdef on_%(handler)s_acivate(self, widget, *args):
%(t)s%(t)sprint widget.get_name()
%(t)sdef %(handler)s(self, str1, str2, int1, int2):
%(t)s%(t)s#context %(class)s.%(handler)s {
%(t)s%(t)swidget = Decimal(str1,str2,int1,int2)
%(t)s%(t)swidget.connect('activate',self.on_%(handler)s_acivate)
%(t)s%(t)swidget.show_all()
%(t)s%(t)sreturn widget
%(t)s%(t)s#context %(class)s.%(handler)s  %(widget)s }

"""

main_format = """\
def main():
"""

instance_format = """\
%(t)s%(root)s = %(class)s()
"""
run_format = """\

%(t)s%(root)s.run()

if __name__ == "__main__":
%(t)smain()
"""

class NotGladeDocumentException(SAXParseException):
    def __init__(self, glade_writer):
        strerror = "Not a glade-2 document"
        SAXParseException.__init__(self, strerror, None, glade_writer.sax_parser)

class SimpleGladeCodeWriter(xml.sax.handler.ContentHandler):
    def __init__(self, glade_file):
        
        self.indent = "\t"
        self.code = ""
        self.roots_list = []
        self.widgets_stack = []
        self.widgets = {}
        self.creation_functions = []
        self.callbacks = []
        self.parent_is_creation_function = False
        self.glade_file = glade_file
        self.data = {}
        self.data["_class"] = "%(_class)s"
        self._class =None
        self._class_name =None
        self.input_dir, self.input_file = os.path.split(glade_file)
        base = os.path.splitext(self.input_file)[0]
        module = self.normalize_symbol(base)
        self.output_file = os.path.join(self.input_dir, module) + ".py"
        self.sax_parser = xml.sax.make_parser()
        self.sax_parser.setFeature(xml.sax.handler.feature_external_ges, False)
        self.sax_parser.setContentHandler(self)
        self.data["glade"] = self.input_file
        self.data["module"] = module
        self.data["date"] = time.asctime()
        

    def normalize_symbol(self, base):
        return "_".join( re.findall(tokenize.Name, base) )

    def capitalize_symbol(self, base):
        ClassName = "[a-zA-Z0-9]+"
        base = self.normalize_symbol(base)
        capitalize_map = lambda s : s[0].upper() + s[1:]
        return "".join( map(capitalize_map, re.findall(ClassName, base)) )

    def uncapitalize_symbol(self, base):
        InstanceName = "([a-z])([A-Z])"
        action = lambda m: "%s_%s" % ( m.groups()[0], m.groups()[1].lower() )
        base = self.normalize_symbol(base)
        base = base[0].lower() + base[1:]
        return re.sub(InstanceName, action, base)

    def startElement(self, name, attrs):
        if name == "widget":
            widget_id = attrs.get("id")
            widget_class = attrs.get("class")
            self.widgets[widget_id] = len(self.widgets)
            if not widget_id or not widget_class:
                raise NotGladeDocumentException(self)
            if not self.widgets_stack:
                self.creation_functions = []
                self.callbacks = []
                class_name = self.capitalize_symbol(widget_id)
                self.data["class"] = class_name
                self.data["root"] = widget_id
                self.roots_list.append(widget_id)
                if self.data["root"].upper().startswith("FRM"):
                    self.code += class_format_frm % self.data
                elif self.data["root"].upper().startswith("DLG"):
                    self.code += class_format_dlg % self.data
            self.widgets_stack.append(widget_id)
        elif name == "signal":
            if not self.widgets_stack:
                raise NotGladeDocumentException(self)
            widget = self.widgets_stack[-1]
            signal_object = attrs.get("object")
            if signal_object:
                return
            handler = attrs.get("handler")
            if not handler:
                raise NotGladeDocumentException(self)
            if handler.startswith("gtk_"):
                return
            signal = attrs.get("name")
            if not signal:
                raise NotGladeDocumentException(self)
            self.data["widget"] = widget
            self.data["signal"] = signal
            self.data["handler"]= handler
            if handler not in self.callbacks:
                if self.data["widget"] == "btnCerrar":
                    self.code += callback_format_btnCerrar % self.data
                elif self.data["widget"] == "btnAnadir":
                    self.code += callback_format_Anadir % self.data
                elif self.data["widget"] == "btnQuitar":
                    self.code += callback_format_Quitar % self.data
                elif self.data["widget"] == "btnPropiedades":
                    self.code += callback_format_Propiedades % self.data
                else:
                    self.code += callback_format % self.data
                self.callbacks.append(handler)
        elif name == "property":
            if attrs['name'] == 'role':
                self._class = True
            if not self.widgets_stack:
                raise NotGladeDocumentException(self)
            widget = self.widgets_stack[-1]
            prop_name = attrs.get("name")
            if not prop_name:
                raise NotGladeDocumentException(self)
            if prop_name == "creation_function":
                self.parent_is_creation_function = True
        

    def characters(self, content):
        if self._class != None:
            if self._class_name ==None:
                self._class_name = content
                self.data["_class"] = content
        if self.parent_is_creation_function:
            if not self.widgets_stack:
                raise NotGladeDocumentException(self)
            handler = content.strip()
            if handler not in self.creation_functions:
                self.data["handler"] = handler
                self.code += creation_format % self.data
                self.creation_functions.append(handler)

    def endElement(self, name):
        if name == "property":
            self.parent_is_creation_function = False
        elif name == "widget":
            if not self.widgets_stack:
                raise NotGladeDocumentException(self)
            self.widgets_stack.pop()
        

    def write(self):
        self.data["t"] = self.indent
        self.code += header_format % self.data
        try:
            glade = open(self.glade_file, "r")
            self.sax_parser.parse(glade)
        except xml.sax._exceptions.SAXParseException, e:
            sys.stderr.write("Error parsing document\n")
            return None
        except IOError, e:
            sys.stderr.write("%s\n" % e.strerror)
            return None

        self.code += main_format % self.data

        for root in self.roots_list:
            self.data["class"] = self.capitalize_symbol(root)
            self.data["root"] = self.uncapitalize_symbol(root)
            self.code += instance_format % self.data

        self.data["root"] = self.uncapitalize_symbol(self.roots_list[0])
        self.code += run_format % self.data
        self.code += "#"
        for i in self.widgets:
            self.code += " %s"%(i)
        try:
            self.output = codecs.open(self.output_file, "w", "utf-8")
            self.output.write(self.code %(self.data))
            self.output.close()
        except IOError, e:
            sys.stderr.write("%s\n" % e.strerror)
            return None
        return self.output_file

def usage():
    program = sys.argv[0]
    print """\
Write a simple python file from a glade file.
Usage: %s <file.glade>
""" % program

def which(program):
    if sys.platform.startswith("win"):
        exe_ext = ".exe"
    else:
        exe_ext = ""
    path_list =  os.environ["PATH"].split(os.pathsep)
    for path in path_list:
        program_path = os.path.join(path, program) + exe_ext
        if os.path.isfile(program_path):
            return program_path
    return None

def check_for_programs():
    packages = {"diff" : "diffutils", "patch" : "patch"}
    for package in packages.keys():
        if not which(package):
            sys.stderr.write("Required program %s could not be found\n" % package)
            sys.stderr.write("Is the package %s installed?\n" % packages[package])
            if sys.platform.startswith("win"):
                sys.stderr.write("Download it from http://gnuwin32.sourceforge.net/packages.html\n")
            sys.stderr.write("Also, be sure it is in the PATH\n")
            return False
    return True

def main():
    if not check_for_programs():
        return -1
    if len(sys.argv) == 2:
        code_writer = SimpleGladeCodeWriter( sys.argv[1] )
        glade_file = code_writer.glade_file
        output_file = code_writer.output_file
        output_file_orig = output_file + ".orig"
        output_file_bak = output_file + ".bak"
        short_f = os.path.split(output_file)[1]
        short_f_orig = short_f + ".orig"
        short_f_bak = short_f + ".bak"
        helper_module = os.path.join(code_writer.input_dir,SimpleGladeApp_py)
        custom_diff = "custom.diff"

        exists_output_file = os.path.exists(output_file)
        exists_output_file_orig = os.path.exists(output_file_orig)
        if not exists_output_file_orig and exists_output_file:
            sys.stderr.write('File "%s" exists\n' % short_f)
            sys.stderr.write('but "%s" does not.\n' % short_f_orig)
            sys.stderr.write("That means your custom code would be overwritten.\n")
            sys.stderr.write('Please manually remove "%s"\n' % short_f)
            sys.stderr.write("from this directory.\n")
            sys.stderr.write("Anyway, I\'ll create a backup for you in\n")
            sys.stderr.write('"%s"\n' % short_f_bak)
            shutil.copy(output_file, output_file_bak)
            return -1
        if exists_output_file_orig and exists_output_file:
            os.system("diff -U1 %s %s > %s" % (output_file_orig, output_file, custom_diff) )
            if not code_writer.write():
                os.remove(custom_diff)
                return -1
            shutil.copy(output_file, output_file_orig)
            if os.system("patch -fp0 < %s" % custom_diff):
                os.remove(custom_diff)
                return -1
            os.remove(custom_diff)
        else:
            if not code_writer.write():
                return -1
            try:
                shutil.copy(output_file, output_file_orig)
            except:
                av= os.system("python reindent.pyc  %s" % output_file)
        os.chmod(output_file, 0755)
        if not os.path.isfile(helper_module):
            open(helper_module, "w").write(SimpleGladeApp_content)
        print "Wrote", output_file
        os.system("python reindent.pyc  %s" % output_file)
        return 0
    else:
        usage()
        return -1

SimpleGladeApp_py = "SimpleGladeApp.py"

SimpleGladeApp_content = """\
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
"""

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)