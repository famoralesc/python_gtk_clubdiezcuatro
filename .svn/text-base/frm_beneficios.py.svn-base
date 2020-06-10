#!/usr/bin/env python
# -*- coding: UTF8 -*-


from package import *
#from class_usuario import class_usuario
#from class_cargo import class_cargo
#from ventas import *
glade_dir = "Glade"

from orm.repository import Beneficios
# Put your modules and data here

# From here through main() codegen inserts/updates a class for
# every top-level widget in the .glade file.

class FrmBeneficios(SimpleGladeApp):
    def __init__(self,cnx =None, padre =None, cod_funcion=None,glade_path="frm_beneficios.glade", root="FrmBeneficios", domain=None):
        glade_path = os.path.join(glade_dir, glade_path)
        self.cnx = cnx
        SimpleGladeApp.__init__(self, glade_path, root, domain)
        if padre == None:
            self.padre = self
            self.ventana = self.FrmBeneficios
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
        columnas.append([1, "Descripción del beneficio", "str"])
        columnas.append([2, "Fecha y hora de ingreso", "str"])
#        columnas.append([2, "Nombre Completo", "str"])
#        columnas.append([4,"Lugar de trabajo","str"])

        SimpleTree.GenColsByModel(self.modelo, columnas, self.tree)
        
    def crea_modelo(self):
        '''Crea un modelo basado en gtk.ListStore, en el cual carga
        los datos de la tabla cliente de la base de datos local.
        '''
        self.modelo = gtk.ListStore(str, str, str)

    def carga_datos(self):
        self.modelo.clear()
        for i in self.data.query(Beneficios).all():
            self.modelo.append((i.id, i.descripcion, i.inserttime))
        
        self.data.close()

    def on_btnAnadir_clicked(self, widget, *args):
        
        d = DlgBeneficio(self.cnx, self.padre)
        if d.dlgBeneficio.run() == gtk.RESPONSE_OK:
            self.carga_datos()
            
        d.dlgBeneficio.destroy()

    def on_btnQuitar_clicked(self, widget, *args):
        model,iter = self.tree.get_selection().get_selected()
        if iter != None:
            try:
                Session = orm.sessionmaker(self.cnx)
                self.data = Session()
                beneficio = self.data.query(Beneficios).get(model.get_value(iter,0))
                self.data.delete(beneficio)
                self.data.commit()
                self.carga_datos()
                dlgAviso(self.ventana,"El beneficio fue eliminado exitosamente.")
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
            d = DlgBeneficio(None, self.padre)
            Session = orm.sessionmaker(self.cnx)
            self.data = Session()
            beneficio = self.data.query(Beneficios).get(model.get_value(iter,0))
            
            d.txtDesc_beneficio.set_text(beneficio.descripcion)
#            d.txtLogin.set_text(usuario.username)
#            d.txtPassword.set_text(usuario.password)
            
            if d.dlgBeneficio.run() == gtk.RESPONSE_OK:
                self.carga_datos()
                
            d.dlgBeneficio.destroy()

    def on_btnBuscar_clicked(self, widget, *args):
        #context FrmBeneficios.on_btnBuscar_clicked {
        self.modelo.clear()
        self.carga_datos()
        #context FrmBeneficios.on_btnBuscar_clicked  btnBuscar}

    def on_btnCerrar_clicked(self, widget, *args):
        #context FrmBeneficios.on_btnCerrar_clicked {
        if self.ventana == self.FrmBeneficios:
            self.quit()
        else:
            del self.padre.wins[self.etiqueta]
            self['main_widget'].destroy()
            #self.padre.ntbPrincipal.remove_page(self.padre.ntbPrincipal.get_current_page())
            return 1
        #context FrmUsuario.on_btnCerrar_clicked  btnCerrar}

    def on_treeBanco_row_activated(self, widget, *args):
        #context FrmBeneficios.on_treeBanco_row_activated {
        self.on_btnPropiedades_clicked(None)
        #context FrmBeneficios.on_treeBanco_row_activated  tree}

class DlgBeneficio(SimpleGladeApp):
    def __init__(self,cnx =None, padre =None, glade_path="frm_beneficios.glade", root="dlgBeneficio", domain=None):
        glade_path = os.path.join(glade_dir, glade_path)
        
        SimpleGladeApp.__init__(self, glade_path, root, domain)
        
        if padre == None:
            self.padre = self
            self.ventana = self.dlgBeneficio
            self.dlgBeneficio.maximize()
            self.dlgBeneficio.show()
        else:
            self.padre = padre
            self.ventana = padre.ventana        

    def new(self):
        pass

    def set_data(self,data):
        self.data = data

    def get_data(self):
        return self.data
    
    def aceptar(self):
        Session = orm.sessionmaker(self.padre.cnx)
        self.data = Session()
        beneficio = Beneficios()
        try:
            beneficio.descripcion = self.txtDesc_beneficio.get_text()
            self.data.add(beneficio)
            self.data.commit()
            dlgAviso(self.ventana,"El beneficio se ha registrado")
            self.data.close()
        except:
            self.data.rollback()
            dlgError(self.ventana, "Ocurrio un error al agregar el beneficio")
            self.data.close()

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
