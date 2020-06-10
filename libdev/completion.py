#~ from pyPgSQL.PgSQL import connect
#from verifica_permiso import VerificaPermiso
from PixEntryCompletion import PixEntryCompletion
import gtk
from codificacion import CUTF8
#from libdev.constantes import MESES

class CompletionInstituto(PixEntryCompletion):
    def __init__(self, entry = gtk.Entry(), sel_func = None, cnx = None):
        PixEntryCompletion.__init__(self, entry, selfunc = sel_func, match_all = False)

        self.cnx = cnx

#        self.cursor = self.cnx.cursor()       
        self.carga_modelo()
    
    def carga_modelo(self):        
        sql = """SELECT
                        id,
                        descripcion
                FROM
                        institucion_educacional
                """
        r = self.cnx.execute(sql)

        
        modelo = self.get_model()
        if modelo == None:
            modelo = gtk.ListStore(str, str)
            self.set_model(modelo)
        else: 
            if modelo.get_n_columns()==1:
                modelo = gtk.ListStore(str, str)
                self.set_model(modelo)
        modelo.clear()
        for i in r.fetchall():
            modelo.append((i[1],i[0]))
            
        self.set_select_column(0)

class CompletionBeneficios(PixEntryCompletion):
    def __init__(self, entry = gtk.Entry(), sel_func = None, cnx = None):
        PixEntryCompletion.__init__(self, entry, selfunc = sel_func, match_all = False)

        self.cnx = cnx

#        self.cursor = self.cnx.cursor()       
        self.carga_modelo()
    
    def carga_modelo(self):        
        sql = """SELECT
                        id,
                        descripcion
                FROM
                        beneficios
                """
        r = self.cnx.execute(sql)

        
        modelo = self.get_model()
        if modelo == None:
            modelo = gtk.ListStore(str, str)
            self.set_model(modelo)
        else: 
            if modelo.get_n_columns()==1:
                modelo = gtk.ListStore(str, str)
                self.set_model(modelo)
        modelo.clear()
        for i in r.fetchall():
            modelo.append((i[1],i[0]))
            
        self.set_select_column(0)
