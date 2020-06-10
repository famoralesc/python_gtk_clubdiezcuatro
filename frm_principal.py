#!/usr/bin/env python
# -*- coding: UTF8 -*-
'''
Created on 19-10-2010

@author: felipe
'''

# Python module frm_principal.py
# Autogenerated from frm_principal.glade
# Generated on Mon sep 24 17:24:13 2007

# Warning: Do not delete or modify comments related to context
# They are required to keep user's code

from package import *
#from pyBerMaster import pyBerMaster,  pyBerMasterGril
glade_dir = "Glade"
# Put your modules and data here
# From here through main() codegen inserts/updates a class for
# every top-level widget in the .glade file.

class Principal(GladeConnect):

    def __init__(self, **args):
        GladeConnect.__init__(self, "Glade/frm_principal.glade")
        self.FrmPrincipal.maximize()
#        self.FrmPrincipal.set_icon_from_file("icono.png")
        self.FrmPrincipal.set_title("Registro Club Diez Cuatro")
        self.wins = {}
        self.ventana_activa = None
        self.habilitar_menu(False)
        self.cnx = args.pop('cnx')
        self.on_mnuConectar_activate()
        self.rut_cliente_ultimo = ''
        self.nom_cliente_ultimo = ''
        self.ventana = self.FrmPrincipal
        sys.__setattr__('ventana', self.ventana)
        #self.mnuconsumo.set_property('visible', False)
        
    def habilitar_menu(self, estado=False):
        self.mnuMaestros.set_sensitive(estado)
        self.mnuSistema.set_sensitive(estado)
        
     
    def on_mnuConectar_activate(self, widget=None, *args):
        d = dlgConeccion(None, None, None,self.on_mnuDesconectar_activate)
        usuario = d.execute(self.cnx)
        self.usuario = d.txtUsuario.get_text()
        d.destroy() 
        if not usuario:
            return
        else:
            sys.__setattr__('cnx', self.cnx)
            sys.__setattr__('usuario', usuario)
            self.entNombre.set_text(usuario.nombre_completo)
            self.entEmpresa.set_text('Club Diez Cuatro Talca')
            self.habilitar_menu(True)

    def on_mnuusuarios_activate(self, widget, *args):
        from frm_usuario import FrmUsuarios

        usuario = sys.usuario
        if not permisos.verifica_permiso(usuario, permisos.USUARIOS):
            dlgAviso(self.ventana, 'No tiene permisos para ejecutar la acción')
            return
        a = FrmUsuarios(self.cnx, self)
        self._nueva_pagina(a.vboxUsuario, "Gestión de Usuarios")
        a.etiqueta = 'Gestión de Usuarios'
    
    def on_mnubeneficios_activate(self, widget, *args):
        from frm_beneficios import FrmBeneficios#TODO: permisos para entrega        
        usuario = sys.usuario
        
        if not permisos.verifica_permiso(usuario, permisos.BENEFICIOS):
            dlgAviso(self.ventana, 'No tiene permisos para ejecutar la acción')
            return
        a = FrmBeneficios(self.cnx, self)
        self._nueva_pagina(a.vboxBeneficios, "Gestión de Beneficios")
        a.etiqueta='Gestión de Beneficios'
        
    def on_mnuinstituciones_activate(self,  widget,  *args):
        from frm_institucion_educacional import frmInstitucionEducacional
        
        usuario = sys.usuario
        
        if not permisos.verifica_permiso(usuario, permisos.INSTITUCIONES):
            dlgAviso(self.ventana, 'No tiene permisos para ejecutar la acción')
            return
        a=frmInstitucionEducacional(self.cnx, self)
        self._nueva_pagina(a.vboxInstitucion, "Gestión de Instituciones Educacionales")
        a.etiqueta='Gestión de Instituciones Educacionales'
        
    def on_mnuregistro_cliente_activate(self, widget, *args):
        from frm_clientes import FrmClientes
        
        usuario = sys.usuario
        if not permisos.verifica_permiso(usuario, permisos.REG_CLIENTES):
            dlgAviso(self.ventana, 'No tiene permisos para ejecutar la acción')
            return
        
        a = FrmClientes(self.cnx, self)
        self._nueva_pagina(a.vboxCliente, "Registro de Clientes")
        a.etiqueta = 'Registro de Clientes'
        
    def on_mnuDesconectar_activate(self, widget, *args):
        self.cnx = None
        self.usuario = None
        self.cursor = None
        while self.ntbPrincipal.get_n_pages() > 0:
            self.ntbPrincipal.remove_page(-1)
        self.wins = {}
        self.ventana_activa = None
        self.habilitar_menu(False)

    def _nueva_pagina(self, widget, label):
        p = -1
        if not self.wins.has_key(label):
            v = gtk.VBox()
            l = gtk.Label('')
            l.set_text_with_mnemonic(label)
            widget.unparent()
            self.ntbPrincipal.append_page(widget, l)
            widget.set_size_request(0, 0)
            widget.show()
            self.wins[label] = (v, widget, len(self.wins))
        else:
            #self.ntbPrincipal.show_all()
            self.ntbPrincipal.set_current_page(self.wins[label][2])
            a = self.ntbPrincipal.get_current_page()
        p = len(self.wins) - 1
        self.ntbPrincipal.set_current_page(-1)
        return p

    def on_btnSalir_clicked(self, widget, *args):
        #context DlgAcercaDe.on_btnSalir_clicked {
        self.quit()
        #context DlgAcercaDe.on_btnSalir_clicked }
    
    def on_mnuSalir_activate(self, widget, *args):
        if self.ntbPrincipal.get_n_pages() > 0:
            d = dlgSiNo(self.FrmPrincipal, 'Existen ventanas abiertas, ¿Está Seguro?')
            if d.response == gtk.RESPONSE_YES:
                self.on_exit()
                #self.quit()
        else:
            self.on_exit()
            
    
            #self.quit()
#if __name__ == '__main__':
#    v = FrmPrincipal(None, None)
#    sys.excepthook = debugwindow.show
#    gtk.threads_init()
#    gtk.threads_enter()
#    gtk.main()    