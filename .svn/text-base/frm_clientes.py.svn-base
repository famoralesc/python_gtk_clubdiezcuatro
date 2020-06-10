#!/usr/bin/env python
# -*- coding: UTF8 -*-


from package import *
from libdev.completion import CompletionInstituto, CompletionBeneficios
from decimal import Decimal, InvalidOperation
from libdev.validar_email import isAddressValid
try:
    import pyfprint
except ImportError as e:
    print e
    
#from class_usuario import class_usuario
#from class_cargo import class_cargo
#from ventas import *
glade_dir = "Glade"
from orm.repository import Clientes, RegistroVisita, BeneficioCliente
# Put your modules and data here

# From here through main() codegen inserts/updates a class for
# every top-level widget in the .glade file.

class FrmClientes(SimpleGladeApp):
    def __init__(self,cnx =None, padre =None, cod_funcion=None,  glade_path="frm_clientes.glade", root="FrmCliente", domain=None):
        glade_path = os.path.join(glade_dir, glade_path)
        self.cnx = cnx
        SimpleGladeApp.__init__(self, glade_path, root, domain)
        if padre == None:
            self.padre = self
            self.ventana = self.FrmClientes
            self.FrmCliente.maximize()
            self.FrmCliente.show()
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
        columnas.append([1, "Nombres", "str"])
        columnas.append([2, "Apellidos", "str"])
        columnas.append([3, "Correo Eléctronico", "str"])
        columnas.append([4, "Edad", "str"])
        columnas.append([5, "# Visitas", "str"])
        columnas.append([6, "Fecha de última visita", "str"])
        SimpleTree.GenColsByModel(self.modelo, columnas, self.tree)
        
    def crea_modelo(self):
        '''Crea un modelo basado en gtk.ListStore, en el cual carga
        los datos de la tabla cliente de la base de datos local.
        '''
        self.modelo = gtk.ListStore(str, str, str, str, str, str, str)

    def carga_datos(self):
        self.modelo.clear()
        self.clientes = self.cnx.execute("""select c.*, rv.fecha_visita from cliente c
                            left join registro_visitas rv 
                                on (c.ultima_visita = rv.id)
                            order by c.id""")
        for i in self.clientes.fetchall():
            self.modelo.append((i.id, i.nombres, i.apellidos, i.email, 
                                i.edad, i.cantidad_visitas, i.fecha_visita))
        
        self.data.close()

    def on_btnAnadir_clicked(self, widget, *args):
        
        d = DlgCliente(self.cnx, self.padre)
        self.padre.clientes = self.clientes
        if d.dlgCliente.run() in (gtk.RESPONSE_CANCEL, gtk.RESPONSE_CLOSE, gtk.RESPONSE_ACCEPT):
            self.carga_datos()
            
        d.dlgCliente.destroy()
        
#    def on_btnRegistrar_clicked(self, widget, *args):
#        d = DlgCliente(self.cnx, self.padre)
#        self.padre.clientes = self.clientes
#        if d.dlgCliente.run() in (gtk.RESPONSE_CANCEL, gtk.RESPONSE_CLOSE, gtk.RESPONSE_ACCEPT):
#            self.carga_datos()
#            
#        d.dlgCliente.destroy()

    def on_btnQuitar_clicked(self, widget, *args):
        model,iter = self.tree.get_selection().get_selected()
        if iter != None:
            try:
                Session = orm.sessionmaker(self.cnx)
                self.session = Session()
                cliente = self.session.query(Clientes).get(model.get_value(iter, 0))
                
                elemento = dict(id = cliente.id, fingers = cliente.huella_digital)
                
                self.session.delete(cliente)
                self.session.commit()
                self.carga_datos()
                dlgAviso(self.ventana,"El fue eliminado exitosamente.")
                
                cache = sys.cache
                self.finger_cache = cache.get('fingers')
                self.finger_cache.remove(elemento)
                cache.replace('fingers', self.finger_cache)
                
            except:
                self.session.rollback()
                dlgError(self.ventana, 
                         "Ocurrio un error al eliminar a %s"%(
                                                        model.get_value(iter,1))
                         )
                
            self.session.close()
            
    def on_btnPropiedades_clicked(self, widget, *args):

        model,iter = self.tree.get_selection().get_selected()
        if iter != None:
            d = DlgCliente(None, self.padre)
            Session = orm.sessionmaker(self.cnx)
            self.data = Session()
            clientes = self.data.query(Clientes).get(model.get_value(iter,0))
            
            d.txtDesc_usuario.set_text(clientes.nombres)
            d.txtLogin.set_text(clientes.username)
            d.txtPassword.set_text(clientes.password)
            
            if d.dlgCliente.run() in (gtk.RESPONSE_OK, gtk.RESPONSE_CANCEL):
                self.carga_datos()
                
            d.dlgCliente.destroy()

    def on_btnBuscar_clicked(self, widget, *args):
        #context FrmBeneficios.on_btnBuscar_clicked {
        self.modelo.clear()
        self.carga_datos()
        #context FrmBeneficios.on_btnBuscar_clicked  btnBuscar}

    def on_btnCerrar_clicked(self, widget, *args):
        #context FrmBeneficios.on_btnCerrar_clicked {
        if self.ventana == self.FrmCliente:
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

class DlgCliente(SimpleGladeApp):
    def __init__(self,cnx =None, padre =None, glade_path="frm_clientes.glade", root="dlgCliente", domain=None):
        glade_path = os.path.join(glade_dir, glade_path)
        SimpleGladeApp.__init__(self, glade_path, root, domain)
        
        if padre == None:
            self.padre = self
            self.ventana = self.dlgCliente
            self.dlgCliente.maximize()
            self.dlgCliente.show()
        else:
            self.padre = padre
            self.ventana = padre.ventana        
        
        self.cargar_info_dispositivo()
        
        self.get_data()
        self.usuario = sys.usuario
        
        self.intentar_verificar = True
        self.intentos = 0
        self.pecInstituto = CompletionInstituto(entry = self.entryInstituto, cnx = cnx)
        if permisos.verifica_permiso(self.usuario, permisos.ASING_BENEFICIOS):
            self.pecBeneficio = CompletionBeneficios(entry = self.entryBeneficio, cnx = cnx)
        else:
            self.entryBeneficio.set_sensitive(False)
            
    def new(self):
        #self.inicializar_dispositivo()
        pass
    
    def validar_formulario(self):
        #validar que los campos obligatorios se llenen
        if not self.txtRut.get_text():
            dlgError(self.ventana, "El RUT es obligatorio", trace= False)
            return False
        if not self.txtNombres.get_text():
            dlgError(self.ventana, "A lo menos el nombre es obligatorio", trace= False)
            return False
        if not self.txtEmail.get_text():
            dlgError(self.ventana, "El e-mail es obligatorio", trace= False)
            return False
        else:
            if not isAddressValid(self.txtEmail.get_text()):
                dlgError(self.ventana, "El e-mail proporcionado no es correcto", trace= False)
                return False   
        
        if not self.txtEdad.get_text():
            dlgError(self.ventana, "La edad de la persona es obligatiria", trace= False)
            return False
        else:
            edad = self.txtEdad.get_text()
            try:
                edad = int(edad)
            except ValueError:
                dlgError(self.ventana, "La edad dede ser un entero", trace= False)
                return False
            if edad < 14 or edad > 150:
                dlgError(self.ventana, "La edad de la persona no puede ser menor a 14 años ni mayor que 150", trace= False)
                return False
        
        if not self.pecInstituto.get_selected():
            dlgError(self.ventana, "Selecciona a lo menos un instituto o universidad", trace= False)
            return False
#        if not self.fingers_to_save:
#            dlgError(self.ventana, "Recuerda escanear la huella digital de la persona", trace= False)
#            return False
        return True
    
    def limpiar_formulario(self):
        self.txtRut.set_text('')
        self.txtNombres.set_text('')
        self.txtApellidos.set_text('')
        self.txtEmail.set_text('')
        self.txtEdad.set_text('')
#        self.pecInstituto.set_selected()
#        self.pecBeneficio.set_selected()
    
    def inicializar_dispositivo(self):
        if pyfprint.fp_init() is not 0: #Needs to be called before anything else
            dlgError(self.ventana, "Imposible inicializar la libreria para el escaner")
            return

    def cargar_info_dispositivo(self):
        self.fingerdevs = pyfprint.discover_devices() #Finds all the connected devices
        if not self.fingerdevs:
            dlgError(self.ventana, 
                "No hay un escaner de huellas digitales conectado al equipo", trace=False)
            self.dlgCliente.destroy()
            return 
        
        self.dispositivo = self.fingerdevs[0]
        self.dispositivo.open()
        self.txtInfoDispostivo.set_text(
                    self.dispositivo.driver().full_name()
                    )
        
    def set_data(self,session, cliente):
        self.session = session
        self.cliente = cliente

    def get_data(self):
        self.session = None
        self.cliente = None
        cache = sys.cache
        self.finger_cache = cache.get('fingers')
        if self.finger_cache is None:
            self.finger_cache = []
            Session = orm.sessionmaker(self.padre.cnx)
            self.data = Session()
            clientes = self.data.query(Clientes).all()
            for c in clientes:
                self.finger_cache.append(dict(id = c.id,
                                        fingers = c.huella_digital))
            
            cache.set('fingers', self.finger_cache)
        
        self.fingers_list = []
        for finger in self.finger_cache:
            self.fingers_list.append(dict(id = finger['id'], fingers \
                            = pyfprint.Fprint(serial_data = finger['fingers'])))
        
        return self.fingers_list
    
    
    def registrar_visita(self):
        try:
            visita = RegistroVisita()
            visita.cliente_id = self.cliente.id
            visita.fecha_visita = datetime.date.today()
            visita.insertby = self.usuario.username
            self.session.add(visita)
            self.session.flush()
    #        self.session.refresh(visita)
            self.cliente.cantidad_visitas = self.cliente.cantidad_visitas + 1
            self.cliente.ultima_visita = visita.id
        except:
            dlgError(self.ventana, "Imposible registrar al cliente dos veces en un día",
                     trace = False)
            raise
#        self.session.update(self.cliente)
        print "registrar visita"
#        return True
    
    def guardar_cliente(self):
        self.cliente.rut = self.txtRut.get_text()
        self.cliente.nombres = self.txtNombres.get_text()
        self.cliente.apellidos = self.txtApellidos.get_text()
        self.cliente.email = self.txtEmail.get_text()
        self.cliente.edad = self.txtEdad.get_text()
        self.cliente.institucion_educacional_id = self.pecInstituto.get_cod()
        self.cliente.cantidad_visitas = 0
        
        self.cliente.huella_digital = self.fingers_to_save[0].data()
        self.insertby = self.usuario.username
        self.session.add(self.cliente)
        self.session.flush()
#        self.session.refresh(self.cliente)
    
    def asignar_beneficio(self, beneficio_id = None):
        try:
            beneficio = BeneficioCliente()
            beneficio.cliente_id = self.cliente.id
            beneficio.beneficios_id = beneficio_id
            beneficio.insertby = self.usuario.username
            
            self.cliente.beneficios_id = beneficio_id
            self.session.add(beneficio)
            self.session.add(self.cliente)
        except:
            raise
    
    def on_btnSave_clicked(self, widget, *args):
        self.fingers_to_save = []
        d = dlgSiNo(self.ventana, 'Pon el dedo sobre el escaner. Presiona SI cuando estes listo.', 'Confirmar')
        if d.response == gtk.RESPONSE_YES:
            self.enrollar_huella()
            if self.fingers_to_save:
                d = dlgSiNo(self.ventana, '¿Deseas guardar al cliente con esta huella?', 'Confirmar')
                if d.response == gtk.RESPONSE_YES:
                    self.save()
        
    def save(self):
        
        if not self.fingers_to_save:
            dlgAviso(self.ventana, 'Obten la huella antes de guardar un nuevo cliente.')
            return
        
        if not self.validar_formulario():
            return
        
        guardar_en_cache = False
        Session = orm.sessionmaker(self.padre.cnx)
        registrar_visita = True
        if not self.session or not self.cliente:
            self.session = Session()
            self.cliente = Clientes()
            registrar_visita = False
#            self.on_btnObtener_clicked(widget, {'save': True})
        try:
            if not registrar_visita:
                self.guardar_cliente()

                cache = sys.cache
                objeto = dict(id = self.cliente.id,
                                        fingers = self.cliente.huella_digital)
                self.finger_cache.append(objeto)
                guardar_en_cache = True
                
            self.registrar_visita()
            
            if permisos.verifica_permiso(self.usuario, permisos.ASING_BENEFICIOS):
                #si tiene permiso para asignar beneficios
                beneficio_id = self.pecBeneficio.get_cod()
                
                if beneficio_id:
                    if self.cliente.beneficios_id != int(beneficio_id):
                        #Si es distinto al que ya poseia
                        self.asignar_beneficio(int(beneficio_id))
            
            self.session.commit()
            
            if guardar_en_cache:
                if cache.get('fingers'):
                    cache.replace('fingers', self.finger_cache)
                else:
                    cache.set('fingers', self.finger_cache)
                self.fingers_list.append(dict(id = objeto['id'], fingers \
                            = pyfprint.Fprint(serial_data = objeto['fingers']))
                            )
                
            dlgAviso(self.ventana,"El usuario se ha registrado")
            self.limpiar_formulario()
        except:
            self.session.rollback()
            dlgError(self.ventana, "Ocurrio un error al agregar al usuario")
        
        self.session.close()
    
    def on_btnRegistrarVisita_clicked(self, widget, *args):
        '''Para registrar una visita necesitamos obtener y validar la huella de un cliente previamente inscrito
        Al obtener la huella deberiamos registrar al cliente
        '''
        
        self.fingers_to_save = []
        d = dlgSiNo(self.ventana, 'Pon el dedo sobre el escaner. Presiona SI cuando estes listo.', 'Confirmar')
        if d.response == gtk.RESPONSE_YES:
            self.verificar_huella()
            if self.fingers_to_save:
                d = dlgSiNo(self.ventana, '¿La información del cliente es correcta?', 'Confirmar')
                if d.response == gtk.RESPONSE_YES:
                    self.save()
    
    def enrollar_huella(self):
        self.cliente = None
        for enrollstage in xrange(self.dispositivo.nr_enroll_stages()):
            stagedone = False
            while not stagedone:
                print "ENROLAMOS"
                result, huella, im = self.dispositivo.enroll_finger()
                #result = (r, Fprint(data_ptr = fprint), Image(img))
                if result == pyfprint.pyf.FP_ENROLL_COMPLETE:    
                    self.fingers_to_save.append(huella)
#                        self.intentar_verificar = True
                    self.intentos = 0
                    stagedone = True
                elif result == pyfprint.pyf.FP_ENROLL_FAIL:
                    dlgError(self.ventana, "Escaneo invalido", trace = False)
                    stagedone = True
                elif result == pyfprint.pyf.FP_ENROLL_PASS:
                    stagedone = True
                elif result == pyfprint.pyf.FP_ENROLL_RETRY:
                    dlgError(self.ventana, "Escaneo de poca calidad, intentalo nuevamente", trace = False)
                    stagedone = True
                elif result == pyfprint.pyf.FP_ENROLL_RETRY_TOO_SHORT:
                    dlgError(self.ventana, "Necesitas poner el dedo un tiempo más", trace = False)
                    stagedone = True
                elif result == pyfprint.pyf.FP_ENROLL_RETRY_CENTER_FINGER:
                    dlgError(self.ventana, "El dedo no está centrado en el escaner", trace = False)
                    stagedone = True
                elif result == pyfprint.pyf.FP_ENROLL_RETRY_REMOVE_FINGER:
                    dlgAviso(self.ventana, "Quita el dedo del escaner")
                    stagedone = True
            im = im.binarize()
            archivo = 'temp/tmp'
            im.save_to_file(archivo)
            self.imgHuellaDigital.set_from_file(archivo)
            
    def verificar_huella(self):
        self.cliente = None
        self.fingers_temp = [d['fingers'] for d in self.fingers_list]
        print "IDENTIFICAMOS"
        for enrollstage in xrange(self.dispositivo.nr_enroll_stages()):
            stagedone = False
            while not stagedone:
            
                result, huella, im, posicion \
                        = self.dispositivo.identify_finger(self.fingers_temp)
                if result == pyfprint.pyf.FP_VERIFY_NO_MATCH:
                    dlgError(self.ventana, "La huella no esta registrada", trace = False)
                    stagedone = True
                    self.intentos += 1
                elif result == pyfprint.pyf.FP_VERIFY_MATCH:
                    self.cargar_data(self.fingers_list[posicion])
                    self.fingers_to_save = []
                    self.fingers_to_save.append(huella)
                    stagedone = True
                elif result == pyfprint.pyf.FP_VERIFY_RETRY:
                    dlgError(self.ventana, "Escaneo de poca calidad, intentalo nuevamente", trace = False)
                    stagedone = True
                elif result == pyfprint.pyf.FP_VERIFY_RETRY_TOO_SHORT:
                    dlgError(self.ventana, "Necesitas poner el dedo un tiempo más", trace = False)
                    stagedone = True
                elif result == pyfprint.pyf.FP_VERIFY_RETRY_CENTER_FINGER:
                    dlgError(self.ventana, "El dedo no está centrado en el escaner", trace = False)
                    stagedone = True
                elif result == pyfprint.pyf.FP_VERIFY_RETRY_REMOVE_FINGER:
                    dlgAviso(self.ventana, "Quita el dedo del escaner")
                    stagedone = True
            im = im.binarize()
            archivo = 'temp/tmp'
            im.save_to_file(archivo)
            self.imgHuellaDigital.set_from_file(archivo)
    
#    def on_btnObtener_clicked(self, widget, is_check=True, *args):
#        if is_check:
#            self.fingers_temp = [d['fingers'] for d in self.fingers_list]
#        fingers = []
#        self.fingers_to_save = []
#        posicion = None
#
#        if self.intentos >= 2:
#            d = dlgSiNo(self.ventana, '¿Desea registrar al cliente como nuevo?', 'Confirmar')  
#            if d.response == gtk.RESPONSE_YES:
#                self.intentar_verificar = False
#                try:
#                    self.cliente = getattr(self, 'cliente')
#                    self.cliente = None
#                    self.session = None
#                except:
#                    pass
#                
#        for enrollstage in xrange(self.dispositivo.nr_enroll_stages()):
#            stagedone = False
#            while not stagedone:
#                if self.fingers_temp and self.intentar_verificar:
#                    print "IDENTIFICAMOS"
#                    identificar = True
#                    # si hay fingers en la cache
#                    result, huella, im, posicion \
#                            = self.dispositivo.identify_finger(self.fingers_temp)
#                else:
#                    print "ENROLAMOS"
#                    identificar = False
#                    result, huella, im = self.dispositivo.enroll_finger()
#                    #result = (r, Fprint(data_ptr = fprint), Image(img))
#                    
#                if not identificar:
#                    if result == pyfprint.pyf.FP_ENROLL_COMPLETE:    
#                        self.fingers_to_save.append(huella)
#                        self.intentar_verificar = True
#                        self.intentos = 0
#                        stagedone = True
#                    elif result == pyfprint.pyf.FP_ENROLL_FAIL:
#                        dlgError(self.ventana, "Escaneo invalido", trace = False)
#                        stagedone = True
#                    elif result == pyfprint.pyf.FP_ENROLL_PASS:
#                        stagedone = True
#                    elif result == pyfprint.pyf.FP_ENROLL_RETRY:
#                        dlgError(self.ventana, "Escaneo de poca calidad, intentalo nuevamente", trace = False)
#                        stagedone = True
#                    elif result == pyfprint.pyf.FP_ENROLL_RETRY_TOO_SHORT:
#                        dlgError(self.ventana, "Necesitas poner el dedo un tiempo más", trace = False)
#                        stagedone = True
#                    elif result == pyfprint.pyf.FP_ENROLL_RETRY_CENTER_FINGER:
#                        dlgError(self.ventana, "El dedo no está centrado en el escaner", trace = False)
#                        stagedone = True
#                    elif result == pyfprint.pyf.FP_ENROLL_RETRY_REMOVE_FINGER:
#                        dlgAviso(self.ventana, "Quita el dedo del escaner")
#                        stagedone = True
#                else:
#                    if result == pyfprint.pyf.FP_VERIFY_NO_MATCH:
#                        dlgError(self.ventana, "La huella no esta registrada", trace = False)
#                        stagedone = True
#                        self.intentos += 1
#                    elif result == pyfprint.pyf.FP_VERIFY_MATCH:
#                        self.cargar_data(self.fingers_list[posicion])
#                        self.fingers_to_save = []
#                        self.fingers_to_save.append(huella)
#                        stagedone = True
#                    elif result == pyfprint.pyf.FP_VERIFY_RETRY:
#                        dlgError(self.ventana, "Escaneo de poca calidad, intentalo nuevamente", trace = False)
#                        stagedone = True
#                    elif result == pyfprint.pyf.FP_VERIFY_RETRY_TOO_SHORT:
#                        dlgError(self.ventana, "Necesitas poner el dedo un tiempo más", trace = False)
#                        stagedone = True
#                    elif result == pyfprint.pyf.FP_VERIFY_RETRY_CENTER_FINGER:
#                        dlgError(self.ventana, "El dedo no está centrado en el escaner", trace = False)
#                        stagedone = True
#                    elif result == pyfprint.pyf.FP_VERIFY_RETRY_REMOVE_FINGER:
#                        dlgAviso(self.ventana, "Quita el dedo del escaner")
#                        stagedone = True
#                im = im.binarize()
#                archivo = 'temp/tmp'
#                im.save_to_file(archivo)
#                self.imgHuellaDigital.set_from_file(archivo)             
#
#        if args:
#            return fingers
        
    def cargar_data(self, finger):
        id = finger.get('id')
        Session = orm.sessionmaker(self.padre.cnx)
        s = Session()
        cliente = s.query(Clientes).get(id)

        self.txtRut.set_text(cliente.rut)
        self.txtNombres.set_text(cliente.nombres)
        self.txtApellidos.set_text(cliente.apellidos)
        self.txtEmail.set_text(cliente.email or '')
        self.txtEdad.set_text(str(cliente.edad))
        self.pecInstituto.set_cod(cliente.institucion_educacional_id)
        self.pecBeneficio.set_cod(cliente.beneficios_id)
        self.set_data(s, cliente)
        
    def on_btnCancelar_clicked(self, widget, *args):
        self.dispositivo.close()

    def on_btnAceptar_clicked(self, widget, *args):
        self.aceptar()
        
#def main():
#    frm_usuario = FrmClientes()
#    #dlg_usuario = DlgUsuario()
#
#    frm_usuario.run()
#
#if __name__ == "__main__":
#    main()
## dialog-action_area1 scrolledwindow1 lblCodUsuario hbox1 vbox2 dialog-vbox1 btnCancelar lblCargp txtCargo alignment1 dlgUsuario btnBuscar btnCerrar Cod_proyecto FrmBeneficios vboxUsuario lblDescUsuario btnAnadir table1 Txt:Desc_usuario btnQuitar tree btnAceptar toolbar1 btnPropiedades
