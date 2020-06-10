#!/usr/bin/env python
# -*- coding: UTF8 -*-

from package import *
#from class_usuario import class_usuario
#from class_cargo import class_cargo
#from ventas import *
glade_dir = "Glade"

from orm.repository import Usuarios
# Put your modules and data here

# From here through main() codegen inserts/updates a class for
# every top-level widget in the .glade file.

class FrmUsuarios(SimpleGladeApp):
    def __init__(self,cnx =None, padre =None, cod_funcion=None,  glade_path="frm_usuario.glade", root="FrmUsuario", domain=None):
        glade_path = os.path.join(glade_dir, glade_path)
        self.cnx = cnx
        SimpleGladeApp.__init__(self, glade_path, root, domain)
        if padre == None:
            self.padre = self
            self.ventana = self.FrmUsuarios
            self.FrmBeneficios.maximize()
            self.FrmBeneficios.show()
        else:
            self.padre = padre
            self.ventana = padre.ventana
            self.cod_funcion=cod_funcion
        
    def new(self):
        Session = orm.sessionmaker(self.cnx)
        self.data = Session()
        
        self.crea_modelo()
        self.crea_columnas()
        self.carga_datos()

    def crea_columnas(self):
        '''Crea las columnas del gtk.TreeView
        '''
        columnas = []
        columnas.append([0, "ID", "str"])
        columnas.append([1, "Login", "str"])
        columnas.append([2, "Nombre Completo", "str"])
        columnas.append([3, "Es administrador", "boo"])
        columnas.append([4, "Puede registrar clientes", "boo"])
        columnas.append([5, "Puede asignar beneficios", "boo"])
        columnas.append([6, "Puede gestionar usuario", "boo"])
        columnas.append([7, "Puede agregar instituciones", "boo"])
        columnas.append([8, "Puede agregar beneficios", "boo"])
        SimpleTree.GenColsByModel(self.modelo, columnas, self.tree)
        
    def crea_modelo(self):
        '''Crea un modelo basado en gtk.ListStore, en el cual carga
        los datos de la tabla cliente de la base de datos local.
        '''
        self.modelo = gtk.ListStore(str, str, str, bool, bool, bool, bool, bool, bool)
        
    def carga_datos(self):
        self.modelo.clear()
        for i in self.data.query(Usuarios).all():            
            self.modelo.append((i.id, i.username, i.nombre_completo, 
                                i.can_admin, i.can_reg_cliente, 
                                i.can_asing_beneficio, i.can_manage_user, 
                                i.can_add_instituciones, i.can_add_beneficio))
        
        self.data.close()

    def on_btnAnadir_clicked(self, widget, *args):
        
        d = DlgUsuario(self.cnx, self.padre)
        if d.dlgUsuario.run() == gtk.RESPONSE_OK:
            self.carga_datos()
            
        d.dlgUsuario.destroy()

    def on_btnQuitar_clicked(self, widget, *args):
        model,iter = self.tree.get_selection().get_selected()
        if iter != None:
            try:
                Session = orm.sessionmaker(self.cnx)
                self.data = Session()
                usuario = self.data.query(Usuarios).get(model.get_value(iter,0))
                self.data.delete(usuario)
                self.data.commit()
                self.carga_datos()
                dlgAviso(self.ventana,"El fue eliminado exitosamente.")
            except:
                self.data.rollback()
                dlgError(self.ventana, 
                         "Ocurrio un error al eliminar a %s"%(
                                                        model.get_value(iter,1))
                         )
            self.data.close()
            
    def on_btnPropiedades_clicked(self, widget, *args):

        model,iter = self.tree.get_selection().get_selected()
        if iter != None:
            d = DlgUsuario(None, self.padre)
            Session = orm.sessionmaker(self.cnx)
            self.session = Session()
            usuario = self.session.query(Usuarios).get(model.get_value(iter,0))
            
            d.txtDesc_usuario.set_text(usuario.nombre_completo)
            d.txtLogin.set_text(usuario.username)
            d.txtPassword.set_text(usuario.password)
            
            d.chk_canAdmin.set_active(usuario.can_admin)
            d.chk_asingBeneficio.set_active(usuario.can_asing_beneficio)
            d.chk_canAddBeneficio.set_active(usuario.can_add_beneficio)
            d.chk_canRegClientes.set_active(usuario.can_reg_cliente)
            d.chk_canManUser.set_active(usuario.can_manage_user)
            d.chk_canManInstitucion.set_active(usuario.can_add_instituciones)
            
            
            d.set_data(usuario, self.session)
            if d.dlgUsuario.run() == gtk.RESPONSE_OK:
                self.carga_datos()
                
            d.dlgUsuario.destroy()

    def on_btnBuscar_clicked(self, widget, *args):
        #context FrmBeneficios.on_btnBuscar_clicked {
        self.modelo.clear()
        self.carga_datos()
        #context FrmBeneficios.on_btnBuscar_clicked  btnBuscar}

    def on_btnCerrar_clicked(self, widget, *args):
        #context FrmBeneficios.on_btnCerrar_clicked {
        if self.ventana == self.FrmUsuario:
            self.quit()
        else:
            del self.padre.wins[self.etiqueta]
            self['main_widget'].destroy()
            #self.padre.ntbPrincipal.remove_page(self.padre.ntbPrincipal.get_current_page())
            return 1
        #context FrmUsuario.on_btnCerrar_clicked  btnCerrar}

    def on_treeUsuario_row_activated(self, widget, *args):
        #context FrmBeneficios.on_treeBanco_row_activated {
        self.on_btnPropiedades_clicked(None)
        #context FrmBeneficios.on_treeBanco_row_activated  tree}

class DlgUsuario(SimpleGladeApp):
    def __init__(self,cnx =None, padre =None, glade_path="frm_usuario.glade", root="dlgUsuario", domain=None):
        glade_path = os.path.join(glade_dir, glade_path)
        
        SimpleGladeApp.__init__(self, glade_path, root, domain)
        
        if padre == None:
            self.padre = self
            self.ventana = self.dlgUsuario
            self.dlgUsuario.maximize()
            self.dlgUsuario.show()
        else:
            self.padre = padre
            self.ventana = padre.ventana        

    def new(self):
        self.set_data(Usuarios())
        pass

    def set_data(self,data, session = None):
        self.data = data
        self.session = session

    def get_data(self):
        if not self.session:
            Session = orm.sessionmaker(self.padre.cnx)
            self.session = Session()
        return self.data, self.session
    
    def aceptar(self):        
        usuario, session = self.get_data()

        try:
            usuario.nombre_completo = self.txtDesc_usuario.get_text()
            usuario.username = self.txtLogin.get_text()
            usuario.password = self.txtPassword.get_text()
            
            usuario.can_admin = self.chk_canAdmin.get_active()
            usuario.can_asing_beneficio = self.chk_asingBeneficio.get_active()
            usuario.can_add_beneficio = self.chk_canAddBeneficio.get_active()
            usuario.can_reg_cliente = self.chk_canRegClientes.get_active()
            usuario.can_manage_user = self.chk_canManUser.get_active()
            usuario.can_add_instituciones \
                                = self.chk_canManInstitucion.get_active()
            
            session.add(usuario)
            session.commit()
            dlgAviso(self.ventana,"El usuario se ha registrado")
            session.close()
        except:
            session.rollback()
            dlgError(self.ventana, "Ocurrio un error al agregar al usuario")
            session.close()

    def on_btnCancelar_clicked(self, widget, *args):
        pass

    def on_btnAceptar_clicked(self, widget, *args):
        self.aceptar()

#def main():
#    frm_usuario = FrmBeneficios()
#    #dlg_usuario = DlgUsuario()
#
#    frm_usuario.run()
#
#if __name__ == "__main__":
#    main()
## dialog-action_area1 scrolledwindow1 lblCodUsuario hbox1 vbox2 dialog-vbox1 btnCancelar lblCargp txtCargo alignment1 dlgUsuario btnBuscar btnCerrar Cod_proyecto FrmBeneficios vboxUsuario lblDescUsuario btnAnadir table1 Txt:Desc_usuario btnQuitar tree btnAceptar toolbar1 btnPropiedades
