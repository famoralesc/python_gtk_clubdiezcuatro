# (c) Victor Benitez Tejos 2004-2006

import gtk
from comunes import columna_utf8
import pango

def  GenColsByModel(modelo, indices,tree):
    """Genera Las TreeViewColumn a partir de un Modelo, Tomando como Parametros lo
            Siguiente:
        Modelo: gtk.ListStore(n*gType)
        Indice  : Arreglo en en cual se indican las propiedades de las TreeViewColumn
            ("IdColModelo":12,"TituloColumna":"asas","FormatCol":"str","Func":"funct","ColBand":"1","Editable":True,"cc":"CC")
            * Indice[0]: ID Columna del Modelo
            * Indice[1]: Titulo de la Columna
            * Indice[2]: Tipo de La columna (de acuerdo a esto se da Formato a la Vista de los Datos)
            Indice[3]: Se define segun los Tipos:
                                boo: funcion fixed_toggled
                                Otros: [Editable] Columna Que Guarda la Marca de modificacion
            Indice[4]: segun los Tipos
                                boo: editable
                                Otros: SimpleTree.CellCompletion()
            indices[5]: funcio, se utiliza Solo si al momento de editar una celda se nececita lanzar una funcion
    """
    nCols = 0
    for i in indices:
        if i[2] =="boo":
            render = gtk.CellRendererToggle()
            if len(i) ==4:
                if i[3] != False:
                    render.connect('toggled', i[3], modelo)                
            elif len(i) ==5:
                if i[3] != False:
                    render.connect('toggled', i[3], modelo,i[0])                
            else:
                render.connect('toggled', fixed_toggled, modelo,i[0])
                
            column = gtk.TreeViewColumn(i[1], render, active=i[0])
            if len(i) ==4:
                if i[3] != False:
                    column.set_clickable(True)
                    column.connect('clicked', column_click_ok,modelo, tree, i[0],nCols)
            else:
                    column.set_clickable(True)
                    column.connect('clicked', column_click_ok,modelo, tree, i[0],nCols)
        elif i[2] =="pboo":
            render = gtk.CellRendererToggle()
            if len(i) ==4:
                if i[3] != False:
                    render.connect('toggled', i[3], modelo)                
            elif len(i) ==5:
                if i[3] != False:
                    render.connect('toggled', i[3], modelo,i[0][0])                
            else:
                    render.connect('toggled', fixed_toggled, modelo,i[0][0])
                
            column = gtk.TreeViewColumn(i[1], render, active=i[0][0])
            if len(i) ==4:
                if i[3] != False:
                    column.set_clickable(True)
                    column.connect('clicked', column_click_ok,modelo, tree, i[0][0],nCols)
            else:
                    column.set_clickable(True)
                    column.connect('clicked', column_click_ok,modelo, tree, i[0][0],nCols)
            pix = gtk.CellRendererPixbuf()
            #column = gtk.TreeViewColumn(i[1])
            #pix.set_property('cell-background', 'red')
            column.pack_start(pix, True)
            column.set_attributes(pix, stock_id=i[0][1])
        else:
            if i[2] == "pix":
                render = gtk.CellRendererPixbuf()
            else:
                render = gtk.CellRendererText()
            
            if len(i) >= 4:
                if len(i) == 5:
                    render.set_property('mode',gtk.CELL_RENDERER_MODE_EDITABLE)
                    render.connect("editing-started",edited_cc,i[4])
                if len(i) == 6:
                    render.connect("edited",edited_cb,modelo,i[0],i[3],i[5])
                else:
                    render.connect("edited",edited_cb,modelo,i[0],i[3])
                render.set_property('editable',True)
            if i[2] == "pix":
                column = gtk.TreeViewColumn(i[1])
                column.pack_start(render, False)
                column.set_attributes(render, stock_id=i[0])
            else:
                column = gtk.TreeViewColumn(i[1], render, markup=i[0])
                column.set_resizable(True)
            #column.set_attributes(render,markup=i[0])
            if i[2] =="str":#str
                column.set_cell_data_func(render, columna_utf8, i[0])
                column.set_clickable(True)
                column.connect('clicked', column_click,modelo, tree, i[0],nCols)
            elif i[2] =="pstr":#str
                #column.set_cell_data_func(render, columna_utf8, i[0])
                column.set_clickable(True)
                column.connect('clicked', column_click,modelo, tree, i[0][0],nCols)
                pix = gtk.CellRendererPixbuf()
                #column = gtk.TreeViewColumn(i[1])
                column.pack_start(pix, True)
                column.set_attributes(pix, stock_id=i[0][1])
            elif i[2] =="STR":#str
                #column.set_cell_data_func(render, columna_utf8, i[0])
                column.set_clickable(True)
                column.connect('clicked', column_click,modelo, tree, i[0],nCols)
            elif i[2] =="dbl":#float:
                column.set_cell_data_func(render, columna_real, i[0])
                column.set_clickable(True)
                column.connect('clicked', column_click,modelo, tree, i[0],nCols)
            elif i[2] =="int":
                column.set_cell_data_func(render, columna_numerica, i[0])
                column.set_clickable(True)
                column.connect('clicked', column_click,modelo, tree, i[0],nCols)
            elif i[2] =="rut":
                column.set_cell_data_func(render, columna_rut, i[0])
                column.set_clickable(True)
                column.connect('clicked', column_click,modelo, tree, i[0],nCols)
                
            elif i[2] =="dte":
                column.set_clickable(True)
                column.connect('clicked', column_click,modelo, tree, i[0],nCols)
                column.set_cell_data_func(render, columna_fecha, i[0])
            elif i[2] == "pix":
                pass
        
        tree.append_column(column)
        nCols = nCols +1 
        
    tree.set_model(modelo)
def func_seleccion(model=None,search_col=0,key="",iter=None,tree=None):
        match=''
        value = model.get_value(iter, search_col)
        if model.get_column_type(search_col) == gobject.TYPE_INT:
            match =key.upper() in str(value).upper()
        elif model.get_column_type(search_col) == gobject.TYPE_DOUBLE:
            match =key.upper() in str(value).upper()
        else:
            if value not in('',None):
                match =key.upper() in value.upper()
            
        return not match
def fixed_toggled(cell, path, model,col):
        iter = model.get_iter(path)
        fixed = model.get_value(iter, col)
        fixed = not fixed
        model.set(iter, col, fixed)
def column_click_ok(treeColumn= None,modelo = None, tree = None,NColModelo= None,NColTree= None):
        for i in modelo:
            i[NColModelo] = not i[NColModelo]
def column_click(treeColumn= None,modelo = None, tree = None,NColModelo= None,NColTree= None):
            for i in tree.get_columns():
                i.set_sort_indicator(False)
                
            modelo.set_sort_column_id(NColModelo,0)
            tree.set_search_column(NColModelo)
            tree.set_search_equal_func(func_seleccion,tree)
            tree.get_column(NColTree).set_sort_indicator(True)

def edited_cb(cell, path, new_text,modelo=None,col = None,colBand=None,Func=None):
    
    iter = modelo.get_iter(path)
    if modelo.get_column_type(col) == gobject.TYPE_INT:
        modelo.set(iter, col, int(float(new_text)))
    elif modelo.get_column_type(col) == gobject.TYPE_DOUBLE:
        modelo.set(iter, col, float(new_text))
    else:
        modelo.set(iter, col, new_text.upper())
    if colBand != None:
        modelo.set(iter, colBand, True)
    if Func !=None:
        Func(new_text.upper(),modelo,iter,(path))

def edited_cc(cell, editable, path, data):
    """ Define un gtk.EntryCompletion a una celda
        cell : Celda a setear
        editable : gtk.entry
        data : EntryCompletion
    """
    #editable.show_all(True)
    editable.set_completion(data.get_completion())

class CellCompletion:
    """
        Generador de EntryCompletio para SimpleTree
        cnx : Conexion a la Base de Datos
        sql  : Consulta SQL para la obtencion de los Datos
        selfunc: Funcion de verificacion una vez seleccionado un datos
        sql_where: Variable de filtro para la Consulta SQL
    """
    def __init__(self,cnx,sql=None, selfunc=None,sql_where=None, model=None):
    
        self.completion = gtk.EntryCompletion()
        self.sql = sql
        self.sql_where = sql_where
        self.selfunc = selfunc
        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        #self.modelo = ifd.ListStoreFromSQL(self.cnx,sql)
        self.modelo = gtk.ListStore(str,str)
        self.completion.set_model(self.modelo)
        self.completion.connect("match-selected", self.__item_selected)
        self.completion.set_match_func(self.__match)
        self.selcol=0
        self.selcod=1
        self.match_all =False
        self.completion.set_text_column(self.selcol)
        self.model=model
        self.__carga_modelo__()
        
    def __carga_modelo__(self):
        if self.sql != None:
            if self.sql_where != None:
                if self.sql.upper().find("WHERE") != -1:
                    sql = "%s and %s" % (self.sql, self.sql_where)
                    
                else:
                    sql = "%s where %s" % (self.sql, self.sql_where)
                    
            else:
                sql = self.sql
                
            self.cursor.execute(sql)
            r = self.cursor.fetchall()
            self.modelo.clear()
            for i in r:
                self.modelo.append([CUTF8(j) for j in i])
        else:
            self.modelo.clear()
            for i in self.model:
                self.modelo.append([CUTF8(j) for j in i])
                
    def __item_selected(self, completion, model, iter):
        if self.selfunc != None:
            self.selfunc(completion, model, iter)
            
    def set_where(self,where=None):
        self.sql_where = where
        self.__carga_modelo__()
        
    def set_sql(self, sql=None):
        self.sql = sql
        self.__carga_modelo__()
        
    def get_completion(self):
        return self.completion
    
    def __match(self, completion, entrystr, iter, data=None):
        model = completion.get_model()
        modelstr = model[iter][self.selcol]
        modelcod=model[iter][self.selcod]

        if self.match_all:
            return entrystr.upper() == modelstr.upper()[:len(entrystr.upper())]
            
        else:
            return entrystr.upper() in modelstr.upper()
            
