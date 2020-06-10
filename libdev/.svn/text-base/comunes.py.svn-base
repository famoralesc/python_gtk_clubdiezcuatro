from GladeConnect import GladeConnect
import sys
import string
import gobject
import gtk
import time
import os
from types import StringType
import math
from pyBusqueda import *
from dialogos import *
#from libdev.fechas import ND, CDateLocal, CDateDB
from completion import *
#from verifica_permiso import VerificaPermiso
from codificacion import *
from constantes import *
#from coneccion_pg import *
from widgets.SignedIntegerEntryField import SignedIntegerEntryField as Interger
from widgets.SignedDecimalEntryField import SignedDecimalEntryField as Decimal
from widgets.UnsignedIntegerEntryField import UnsignedIntegerEntryField as UnsignedIntegerEntry
from widgets.DateWidget import DateWidget as Date
from widgets.RUTEntryField import RUTEntryField as Rut
from widgets.CustomEntryField import CustomEntryField as Entry
from widgets.NameEntryField import NameEntryField as Name
from widgets.NameLetterEntryField import NameLetterEntryField as NameLetter
if sys.platform=="win32":
    impresora = 'lpt1:'
else:
    impresora = 'lpr:'
def CNumDb(s):

    if type(s) == float:
        return str(s)

    s = str(s)
    p = len(s)
    t = ""
    for i in range(p):
        c = s[i]
        if c == ',':
            t = t + "."

        elif not c == ".":
            t = t + c

    return t


def CMon(s, dec = 2):
    try:
        A = float(s)
        s = CNumDb(A)
    except:
        #print "ret", s
        return s
    if type(dec) == int:
        c = s.find(".")
        if dec == 0:
            if c <> -1:
                s = s[:c]
        else:
            if len(s[c+1:]) < dec:
                s = s + string.zfill("", dec - len(s[c+1:]))
            s = s[:c + 1 + dec]
    s = s.replace(" ","")
    s = s.replace(".", ",")
    c = s.find(",")
    p = len(s)
    if not c == -1:
        if c < p - 3:
            st = c

        else:
            st = p - (p - c)
    else:
        st = p - 3


    for i in range(st, s[0] in ('+','-'),-3):

        if not s[i] == ",":

            s = s[:i] + '.' + s[i:]

    return s

def columna_numerica(tree, cell, model, iter, data = 0):

    pyobj = model.get_value(iter, data)
    if pyobj !=None:
        pyobj = str(pyobj)
        pyobj = CMon(pyobj, 0)
        cell.set_property('text', pyobj)
    cell.set_property('xalign', 1)

def columna_real(tree, cell, model, iter, data = 0):

    pyobj = model.get_value(iter, data)
    if pyobj !=None:
        pyobj =CMon(str(pyobj), 2)
        cell.set_property('text', pyobj)
    cell.set_property('xalign', 1)


def columna_rut(tree, cell, model, iter, data = 0):

    pyobj = model.get_value(iter, data)
    cell.set_property('text', CRut(pyobj))
    cell.set_property('xalign', 1)

def columna_fecha(tree, cell, model, iter, data = 0):

    pyobj = model.get_value(iter, data)
    cell.set_property('text', CDateLocal(pyobj))
    cell.set_property('xalign', 1)


def columna_utf8(tree, cell, model, iter, data = 0):

    pyobj = model.get_value(iter, data).__str__()
    if pyobj in (None, "None"):
        pyobj =""
    
#    if len(pyobj.split('\n')) != 1:
#        pyobj = pyobj.split('\n')[0] +"..."
#    else:
#        pyobj = pyobj.split('\n')[0]
    try:
        cell.set_property('text', CUTF8(pyobj))
    except:
        cell.set_property('text', CUTF8(pyobj, 'latin1'))


def CRut(rut):
    if rut == "":
        return rut

    rut = string.replace(rut,".","")
    rut = string.replace(rut,"-","")
    rut = "0000000000"+ rut
    l = len(rut)
    rut_aux = "-" + rut[l-1:l]
    l = l-1
    while 2 < l:
        rut_aux = "."+ rut[l-3:l] +rut_aux
        l = l-3

    rut_aux = rut[0:l] +rut_aux
    l = len(rut_aux)
    rut_aux = rut_aux[l-12:l]
    return rut_aux



def iif(condicion, si, no):
    if condicion:
        return si
    else:
        return no


def end_match(completion=None, key=None, iter=None, column=None):
    model = completion.get_model()
    text = model.get_value(iter, column)
    key = unicode(key,'latin1').encode('utf-8')
    if unicode(text,'latin1').encode('utf-8').upper().find(key.upper()) <> -1:
        return True
    return False

def Abre_pdf(arch):
    if sys.platform=="win32":
        acrord = 'c:\\Archivos de programa\\Adobe\\Acrobat 5.0\\Reader\\AcroRd32.exe'

        #~ acrord = "explorer.exe"
        #~ acrord = os.getcwd() + "\\pdfreader\\pdfreader.exe"

        args = [acrord, "AcroRd32.exe",arch]

        try:
            os.spawnv(os.P_NOWAIT, args[0], args[1:])
        except:
            acrord = os.getcwd() + "\\pdfreader\\pdfreader.exe"
            args = [acrord, "pdfreader.exe",arch]
            try:
                os.spawnv(os.P_NOWAIT, args[0], args[1:])
            except:
                pass
    else:
        if os.spawnv(os.P_WAIT, '/usr/bin/evince', ['evince', arch]) == 0:
            return
        if os.spawnv(os.P_WAIT, '/usr/bin/xpdf', ['xpdf', arch]) == 0:
            return
        if os.spawnv(os.P_WAIT, '/usr/bin/acroread', ['acroread', arch]) == 0:
            return
        if os.spawnv(os.P_WAIT, '/usr/bin/gpdf', ['gpdf', arch]) == 0:
            return

def IsNull(valor):
    if valor == None:
        return True
    else:
        return False
def limpia_forma(widget,modelo= True):
    if type(widget) in (gtk.Entry,Rut,Decimal,Interger,Date):
        widget.set_text("")
    if type(widget) == gtk.TextView:
            buf = widget.get_buffer()
            buf.set_text("")
            widget.set_buffer(buf)
    if type(widget) == gtk.TreeView and modelo :
        m = widget.get_model()
        m.clear()
    try:
        if not type(widget) in (gtk.Label,gtk.Image,gtk.Entry):
            
            for i in widget.get_children():
                limpia_forma(i)
    except:
        pass    
if __name__ == '__main__':

    print CMon("100000.0".replace(".",","), 2)
def Numlet(tyCantidad):
    _ret = None
    tyCantidad = round(tyCantidad)
    lyCantidad = int(tyCantidad)
    lyCentavos = ( tyCantidad - lyCantidad )  * 100
    laUnidades = ('UN', 'DOS', 'TRES', 'CUATRO', 'CINCO', 'SEIS', 'SIETE', 'OCHO', 'NUEVE', 'DIEZ', 'ONCE', 'DOCE', 'TRECE', 'CATORCE', 'QUINCE', 'DIECISEIS', 'DIECISIETE', 'DIECIOCHO', 'DIECINUEVE', 'VEINTE', 'VEINTIUN', 'VEINTIDOS', 'VEINTITRES', 'VEINTICUATRO', 'VEINTICINCO', 'VEINTISEIS', 'VEINTISIETE', 'VEINTIOCHO', 'VEINTINUEVE')
    laDecenas = ('DIEZ', 'VEINTE', 'TREINTA', 'CUARENTA', 'CINCUENTA', 'SESENTA', 'SETENTA', 'OCHENTA', 'NOVENTA')
    laCentenas =('CIENTO', 'DOSCIENTOS', 'TRESCIENTOS', 'CUATROCIENTOS', 'QUINIENTOS', 'SEISCIENTOS', 'SETECIENTOS', 'OCHOCIENTOS', 'NOVECIENTOS')
    lnNumeroBloques = 1
    while 1:
        lnPrimerDigito = 0
        lnSegundoDigito = 0
        lnTercerDigito = 0
        lcBloque = ''
        lnBloqueCero = 0
        for i in range(1,4):
            lnDigito = lyCantidad % 10
            if lnDigito <> 0:
                _select0 = i
                if (_select0 == 1):
                    lcBloque = ' ' + laUnidades[lnDigito - 1]
                    lnPrimerDigito = lnDigito
                elif (_select0 == 2):
                    if lnDigito <= 2:
                        lcBloque = ' ' + laUnidades[( lnDigito * 10 )  + lnPrimerDigito - 1]
                    else:
                        lcBloque = ' ' + laDecenas[lnDigito - 1] + iif(lcBloque!='',' Y'+ lcBloque,'')
                    lnSegundoDigito = lnDigito
                elif (_select0 == 3):
                    if lnDigito == 1 and lnPrimerDigito == 0 and lnSegundoDigito == 0:
                        lcBloque = ' ' + 'CIEN'+ lcBloque
                    else:
                        lcBloque = ' ' + laCentenas[lnDigito - 1] + lcBloque
                    lnTercerDigito = lnDigito
            else:
                lnBloqueCero = lnBloqueCero + 1
            lyCantidad = int(lyCantidad / 10)
            if lyCantidad == 0:
                break
        _select1 = lnNumeroBloques
        if (_select1 == 1):
            _ret = lcBloque
        elif (_select1 == 2):
            _ret = lcBloque + IIf(lnBloqueCero == 3, '', ' MIL') + _ret
        elif (_select1 == 3):
            _ret = lcBloque + IIf(lnPrimerDigito == 1 and lnSegundoDigito == 0 and lnTercerDigito == 0, ' MILLON', ' MILLONES') + _ret
        lnNumeroBloques = lnNumeroBloques + 1
        if lyCantidad == 0:
            break
    _ret = _ret + IIf(tyCantidad > 1, ' PESOS ', ' PESO ') #+ Format(Str(lyCentavos), '00') + '/100 M.N. )'
    if _ret[:10]!=' UN MILLON':
        return IIf(_ret[:7]==' UN MIL',' MIL '+_ret[8:],_ret)
    else:
       return  _ret    

def IIf(cond, si, no):
    if cond:
        return si
    else:
        return no
def isNull(valor):
    if valor == None:
        return True
    else:
        return False
