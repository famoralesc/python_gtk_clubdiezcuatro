# -*- coding: utf-8 -*-

#   This file is part of emesene.
#
#    Emesene is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    Emesene is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with emesene; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#    Libreria que permite crear menu desplegable o popup
#    Ricardo Mendez Lorca

import gtk

class PopupMenu(gtk.Menu):
    def __init__(self,dictoption):       
        gtk.Menu.__init__(self)
        self.dictoption=dictoption                
        self.makePopupConfig()
        self.show_all()
    
    def makePopupConfig(self):
        for i in self.dictoption:
            optionpopup=self.newImageMenuItem(i,self.dictoption[i])
            self.add(optionpopup)    
    def newImageMenuItem(self, label, stock=None, img=None, animation=None):
        mi = gtk.ImageMenuItem(label)

        if stock != None:
            mi.set_image(gtk.image_new_from_stock(stock, gtk.ICON_SIZE_MENU))
        elif img != None:
            image = gtk.Image()
            image.set_from_pixbuf(img)
            mi.set_image(image)
        elif animation != None:
            image = gtk.Image()
            image.set_from_animation(animation)
            mi.set_image(image)
        return mi
##
## dictevent diccionario 0:indice 1 func_callback
##dictoption diccionario con los eventos del menu desplegable
##indice label
##valor 1:icono
##dictoption={"Agregar...":gtk.STOCK_ADD,"Quitar":gtk.STOCK_DELETE,"Buscar":gtk.STOCK_FIND,"Error":gtk.STOCK_DIALOG_ERROR} 
##dictevent={"Agregar...":("activate",self.agregar_activate)}    
##    
def build_pop_up(self,menu,dictevent):
        for i in menu:            
            if dictevent.has_key(i.child.get_label()):
                i.connect(dictevent[i.child.get_label()][0],dictevent[i.child.get_label()][1])
def main():
    ##dictoption diccionario con los eventos del menu desplegable
    ##indice label
    ##valor 0:icono
    ##        1:eventos
    ##        2:callback    
    dictoption={"_Add contact...":gtk.STOCK_ADD}
    p=PopupMenu(dictoption)   
if __name__ == "__main__":
    main()
