#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PixEntryCompletion -- Widget especializado para el autcompletado
# (c) Fernando San Martín Woerner 2003, 2004, 2005
# snmartin@galilea.cl

# This file is part of Gestor.
#
# Gestor is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyGestor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import gtk
from gtk import Dialog
from codificacion import CUTF8
from dialogos import dlgBarraProgreso,muestra_splash, splash
class PixEntryCompletion:
    def __init__(self, entry = gtk.Entry(), modelo = None, selcol = 0, selfunc = None, match_all = False,  obj =None,  Master = False):
        if obj==None:
            self.obj = obj
        else:
            self.obj = obj.__class__()
        self.entry = entry
        self.modelo = modelo
        if self.modelo is None:
            cols = 0
            self.modelo = gtk.ListStore(str)
            self.modelo.append([''])
        else:
            cols = len(self.modelo[0])
        self.parent = entry.get_parent()
        self.parent.remove(entry)
        self.hbox = gtk.HBox()
        self.parent.add(self.hbox)
        self.button = gtk.Button()
        self.box_cancel = gtk.HBox(False, 0)
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_NEW, gtk.ICON_SIZE_MENU)
        image.show()
        self.box_cancel.pack_start(image, False, False, 3)
        self.box_ok = gtk.HBox(False, 0)
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_OK, gtk.ICON_SIZE_BUTTON)
        self.box_ok.pack_start(image, False, False, 3)
        image.show()
        self.get_all =True
        self.button.add(self.box_cancel)
        self.box_cancel.show()
        self.hbox.pack_start(entry, True, True)
        self.hbox.pack_start(self.button, False, False)
        self.hbox.show()
        self.button.set_relief(gtk.RELIEF_NONE)
        self.button.show()
        if Master:
            self.button.connect('clicked', self.show_dialog)
        else:
            self.button.connect('clicked', self.search_dialog)
        self.completion = gtk.EntryCompletion()
        self.completion.set_model(self.modelo)
        for i in range(cols):
            if i == selcol:
                self.completion.set_text_column(i)
            else:
                cell = gtk.CellRendererText()
                self.completion.pack_start(cell)
                self.completion.add_attribute(cell, 'text', i)
        self.entry.set_completion(self.completion)
        self.entry.connect('key-press-event', self.on_entry_key_press_event)
        self.selfunc = selfunc
        self.selcol = selcol
        self.iter = None
        self.completion.connect("match-selected", self.__item_selected)
        self.completion.set_match_func(self.__match)
        self.completion.set_popup_set_width(True)
        self.entry.connect('changed', self.__entry_change)
        #self.entry.connect('grab-focus', self.__entry_grab_fucus)
        self.entry.set_data("selected",False)
        self.tooltips = gtk.Tooltips()
        self.tooltips.set_tip(self.entry, "Presione F1 para ver todos los valores")
        self.selcol = 0
        self.codcol =1
        self.select_text = None
        self.cod =None
        self.selected = None
        self.match_all = match_all
        self.show_popup =False

    def __match(self, completion, entrystr, iter, data=None,todo = True):
        model = completion.get_model()
        modelstr = model[iter][self.selcol]
        if todo:
            show_popup = len(model)<=10
        else:
            show_popup = todo
        if entrystr is None or modelstr is None:
            return
        else:
            if show_popup:
##                print "popup"
                return True
            elif self.match_all:
##                print "ALL"
                return entrystr.upper() == modelstr.upper()[:len(entrystr.upper())]
            else:
##                print "otro"
                return entrystr.upper() in modelstr.upper()
    
    def __item_selected(self, completion, model, iter):

        self.select_text = model.get_value(iter, self.selcol)
        self.entry.set_text(model.get_value(iter, self.selcol))
        self.cod = model[iter][self.codcol]
        if self.selfunc != None:
            self.selfunc(completion, model, iter)

        self.set_selected(True)
        

    def __entry_grab_fucus(self, entry,*args):
        if len(self.modelo) < 10 and len(self.modelo) > 1 and not self.get_selected():
            #self.show_popup =True
            self.completion.set_property("inline-completion",True)
            #if self.entry.get_text().strip() == "":
            self.entry.set_text(" ")
            self.completion.get_entry().emit("changed")
            #self.show_popup =False

        
    def __entry_change(self, entry):
        if self.get_selected():
            if self.entry.get_text() != self.select_text:
                self.set_selected(False)
            else:
                self.set_selected(True)
        else:
            self.set_selected(False)

    def set_selected(self, selected = False):

        child = self.button.get_child()
        child.hide()
        self.button.remove(child)
        if selected:
            self.button.add(self.box_ok)
            self.box_ok.show()
            self.entry.set_data("selected",True)
        else:
            self.cod=None
            self.button.add(self.box_cancel)
            self.box_cancel.show()
            self.select_text = None
            self.entry.set_data("selected",False)

        self.selected = selected


    def get_selected(self):
        return self.selected

    def set_select_column(self, col = 0):
        self.selcol =  col
        self.completion.set_text_column(col)
        self.entry.set_data("selected",True)

    def get_select_column(self):
        return self.selcol

    def set_select_func(self, func = None):
        self.selfunc = func
    def set_cod(self,cod,col_search=1, col_ret = 0):
        for i in self.modelo:
            if str(cod) == str(i[col_search]):
                self.entry.set_text(i[col_ret])
                self.set_selected(True)
                self.__item_selected(self,self.modelo,i.iter)
                return
    def set_desc(self,desc,col_search=0, col_ret = 1):
        for i in self.modelo:
            if desc.upper() == i[col_search].upper():
                self.entry.set_text(desc)
                self.set_selected(True)
                self.__item_selected(self,self.modelo,i.iter)
                return
    def get_cod(self):
        return self.cod
    def carga_modelo(self):
        if self.obj != None:
            self.modelo.clear()
            if self.get_all:
                func =self.obj.select_all
            else:
                func = self.obj.select_criterial
            #dlg = dlgBarraProgreso()
            #dlg.set_progreso(0)
            s = muestra_splash("Cargando")
            while gtk.events_pending():
                    gtk.mainiteration(False)
            r = func(self.obj)
            
            #max=len(r)
            #cont=1
            for i in [(eval("i.get_desc_%s()"%(self.obj.table)),eval("i.get_cod_%s()"%(self.obj.table))) for i in r]:
                #cod =i[1]
                self.modelo.append(i)
                #Barra Progreso
                #dlg.set_progreso(cont / float(max))
                while gtk.events_pending():
                    gtk.mainiteration(False)
                #cont = cont +1
            #if len(self.modelo)==1 :
                #self.set_cod(cod)
            s.destroy()
    def get_select_func(self):
        return self.selfunc

    def set_model(self, model=None):
        self.completion.set_model(model)
        self.modelo = model
        if len(self.modelo)==1 :
                self.set_cod(self.modelo[0][1])
    def get_model(self):
        return self.modelo
        
    def on_entry_key_press_event(self, entry, event):
        if event.keyval == gtk.keysyms.F1:
            self.search_dialog()
        elif event.keyval == gtk.keysyms.F5:
            self.carga_modelo()
        else:
            if len(self.modelo) <= 10:
                res = False
                self.show_popup =False
                for i in self.modelo:
                    res = res or self.__match(self.completion, entry.get_text(),i.iter,todo=False)
                self.show_popup =True
                if not res:
                    entry.set_text(" ")
                    gtk.gdk.beep()
                    return True
        

    def show_dialog(self, widget = None, data = None):
        from pyBerMaster import pyBerMaster
        b = self.obj.__class__()
        
        w = gtk.Dialog("Agregar %s"%(b.table),  None, 0,  (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK,))
        t = pyBerMaster(b)
        w.vbox.add(t)
        t.show_all()
        w.show_all()
        def resp(*args):
            if args[1] == gtk.RESPONSE_OK:
                a = t.save()
                if a == None:
                    args[0].destroy()
            else:
                args[0].destroy()
        w.connect('response', resp)
        w.run()
    def search_dialog(self,  widget = None, data = None):
        if self.modelo.get_iter_first() in('', None):
            return
        b = PixBusquedaEntry(self.modelo, self.selcol, self.entry.get_text())
        b.run()
        model, iter = b.list.get_selection().get_selected()
        if not iter is None:
            self.entry.set_text(model.get_value(iter, 0))
            m1 = model.filter_new()
            if self.selfunc != None:
                self.selfunc(self.completion, model, iter)
            self.set_selected(True)
        else:
            self.set_selected(False)
        b.destroy()

class PixBusquedaEntry(Dialog):

    def __init__(self, modelo, selcol, texto):

        self.modelo = modelo

        self.selcol = selcol

        self.search_text = texto

        Dialog.__init__(self,
                CUTF8("Búsqueda"),
                None,
                0,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK,))

        self.set_default_size(700,400)

        hbox = gtk.HBox(False, 8)
        hbox.set_border_width(8)
        self.vbox.pack_start(hbox, 1, 1, 0)
        #self.connect('delete-event', self.destroy)

        vbox1 = gtk.VBox(False)
        vbox1.set_border_width(8)
        hbox.pack_start(vbox1, False, False, 1)
        stock = gtk.image_new_from_stock(gtk.STOCK_FIND, gtk.ICON_SIZE_DIALOG)
        vbox1.pack_start(stock, False, False, 0)

        vbox1.pack_start(
                gtk.Label(
                        CUTF8("\n\nDígite el texto a buscar \nen la entrada de filtro\n"+
                        "y presione la tecla INTRO. \n\nLuego haga doble-click \n"+
                        "sobre el ítem deseado \no seleccionelo y\n"+
                        "presione el botón ACEPTAR")), False, False, False)

        vbox1 = gtk.VBox(False)
        vbox1.set_border_width(8)
        hbox.pack_start(vbox1, True, True, 1)

        lbl = gtk.Label('Filtro:')
        vbox1.pack_start(lbl, False, 0)

        self.txtFiltro = gtk.Entry()
        self.txtFiltro.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.txtFiltro.connect('key-press-event', self.on_entry_key_press_cb)
        self.txtFiltro.connect('changed', self.on_entry_changed_cb)

        vbox1.pack_start(self.txtFiltro, 0, 0)
        s = gtk.ScrolledWindow()

        self.list = gtk.TreeView()
        self.list.set_headers_visible(True)
        n = 0
        
        for i in self.modelo[0]:
            column = gtk.TreeViewColumn("", gtk.CellRendererText(), text=n)
            column.connect('clicked', self.column_click,self.modelo, self.list, n,n)
            n = n + 1

            self.list.append_column(column)

        if self.search_text:
            self.txtFiltro.set_text(texto)

        self.list.connect("row-activated", self.on_tree_row_activated)
        selection = self.list.get_selection()
        selection.set_mode('single')
        self.list.set_model(self.modelo)
        self.list.set_headers_visible(True)
        self.list.set_headers_clickable(True)

        vbox1.pack_start(s, 1, 1)

        s.add(self.list)
        self.filter()

        self.show_all()


    def on_entry_key_press_cb(self, entry, event):
        if event.keyval == gtk.keysyms.Return:
            self.filter()
    
    def column_click(self,treeColumn= None,modelo = None, tree = None,NColModelo= None,NColTree= None):
            for i in tree.get_columns():
                i.set_sort_indicator(False)
                
            modelo.set_sort_column_id(NColModelo,0)
            tree.set_search_column(NColModelo)
            tree.get_column(NColTree).set_sort_indicator(True)

    def on_entry_changed_cb(self, entry):
        entry.set_text(entry.get_text())

    def match(self, model, iter, data = None):
        #~ print self.txtFiltro.get_text()
        if len(self.txtFiltro.get_text()) > 0:
            if model.get_value(iter, self.selcol) != None:
                if model.get_value(iter, self.selcol).upper()==None:
                    modelo=''
                else:
                    modelo=model.get_value(iter, self.selcol).upper()
            else:
                modelo =''
            return self.txtFiltro.get_text().upper() in modelo #model.get_value(iter, self.selcol).upper()
        else:
            return True

    def filter(self):

        self.modelfilter = self.modelo.filter_new()

        self.modelfilter.set_visible_func(self.match)

        self.list.set_model(self.modelfilter)

    def on_tree_row_activated(self, tree, row, column):

        model, iter = self.list.get_selection().get_selected()
        if not iter:
            return 0

        self.response(gtk.RESPONSE_OK)

