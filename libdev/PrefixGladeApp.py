#!/usr/bin/env python

#from SimpleGladeApp import SimpleGladeApp
import gtk
import time
from comunes import CMon
# This class is only to show it can be reused
class PrefixActions:
    def __init__(self, add_mandatory_f, set_error_status_f):
        self.mandatories = []
        self.set_error_status = set_error_status_f
        self.add_mandatory = add_mandatory_f
    def prefix_fon(self, widget):
        def validate(widget):
            text = widget.get_text().replace("-","").replace(" ","")
            try:
                if len(text) < 10:
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        def complete(widget, event):
            error = False
            text = widget.get_text().replace("-","").replace(" ","")
            aux = "            "
            try:
                if len(text) < 10:
                    text = aux[:10-len(text)] + text
                    error = True
                text = text[0:2]+"-"+text[2:4]+"-"+text[4:]
                widget.set_text(text)
                if error ==False:
                    error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)
        widget.connect("focus-out-event", complete)
    
    def prefix_Fon(self,widget):
        self.prefix_fon(widget)
        self.add_mandatory(widget)
        
    def prefix_enc(self, widget):
        def validate(widget,*args):
            try:
                selected = widget.get_data("selected")
                print selected
                if selected:
                    error = False
                else:
                    error =True
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("focus_out_event", validate)
    
    def prefix_Enc(self,widget):
        self.prefix_enc(widget)
        self.add_mandatory(widget)
    
    def prefix_eml(self, widget):
        def validate(widget):
            text = widget.get_text()
            try:
                if text.find("@") == -1 or text.find(".")==-1 :
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)
    
    def prefix_Eml(self,widget):
        self.prefix_enc(widget)
        self.add_mandatory(widget)
        
    def prefix_dia(self, widget):
        def validate(widget):
            text = widget.get_text()
            try:
                dia = int(text)
                if dia < 1 or dia > 30:
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)
    
    def prefix_Dia(self,widget):
        self.prefix_dia(widget)
        self.add_mandatory(widget)
        
    def prefix_spn(self, widget):
        def validate(widget):
            text = widget.get_value()
            self.set_error_status(widget, text <= 0)
        widget.connect("changed", validate)
    
    def prefix_Spn(self, widget):
        self.prefix_spn(widget)
        self.add_mandatory(widget)
        
    def prefix_txt(self, widget):
        def validate(widget):
            text = widget.get_text().strip()
            self.set_error_status(widget, len(text) < 1)
        def complete(widget, event):
            text = widget.get_text().strip()
            widget.set_text(text.upper())
        widget.connect("changed", validate)
        widget.connect("focus-out-event", complete)
        
    def prefix_Txt(self, widget):
        self.prefix_txt(widget)
        self.add_mandatory(widget)
    
    def prefix_name(self, widget):
        def validate(widget):
            text = widget.get_text()
            self.set_error_status(widget, len(text) < 1 or len(text) > 16)
        def complete(widget, event):
            text = widget.get_text()
            cap = lambda s: s.capitalize()
            tokens = text.split()
            tokens = map(cap, tokens)
            text = " ".join(tokens)
            widget.set_text(text)
        widget.connect("changed", validate)
        widget.connect("focus-out-event", complete)
    
    def prefix_Name(self, widget):
        self.prefix_name(widget)
        self.add_mandatory(widget)
    
    def prefix_date(self, widget):
        def parse_date(text):
            text = text.replace("/","-")
            (cY,cm,cd) = time.localtime()[0:3]
            try:
                (d,) = time.strptime(text, "%d")[2:3]
                m,Y = cm,cY
            except ValueError:
                try:    
                    (m,d) = time.strptime(text, "%d-%m")[1:3]
                    Y = cY
                except:
                    (Y,m,d) = time.strptime(text, "%d-%m-%Y")[0:3]
            return (Y,m,d)
        def validate(widget):
            text = widget.get_text()
            try:
                parse_date(text)
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        def complete(widget, event):
            text = widget.get_text()
            try:
                (Y,m,d) = parse_date(text)
                text = "%02d-%02d-%d" % (d,m,Y)
                widget.set_text(text)
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)
        widget.connect("focus-out-event", complete)
    
    def prefix_Date(self,widget):
        self.prefix_date(widget)
        self.add_mandatory(widget)
    def prefix_age(self, widget):
        def validate(widget):
            text = widget.get_text()
            try:
                age = int(text)
                if age < 16 or age > 99:
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)
        
    def prefix_cash(self, widget):
        def validate(widget):
            text = widget.get_text()
            try:
                cash = float(text)
                if cash < 0:
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        def complete(widget, event):
            text = widget.get_text()
            try:
                text = CMon(text,0)
                widget.set_text(text)
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        self.add_mandatory(widget)
        widget.connect("changed", validate)
        #widget.connect("focus-out-event", complete)
    def prefix_Cash(self,widget):
        self.prefix_cash(widget)
        self.add_mandatory(widget)
    def prefix_rut(self,widget):
        def Format_Rut(widget, event):
            rut = widget.get_text()
            if rut == "":
                return rut
        
            rut = rut.replace(".","")
            rut = rut.replace("-","")
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
            widget.set_text(rut_aux)
            
        def es_rut(rut=None):
            if not rut: return 0
            es_rut = False
            cadena = "234567234567"
            dig_rut = rut[-1]
            rut = rut.replace(".", "")
            rut = rut[:rut.find("-")]
            rut = rut.replace(" ", '0')
            j, suma, i = 0, 0, len(rut) -1
            while i >= 0:
                    try:
                            suma = suma + (int(rut[i]) * int(cadena[j]))
            
                    except:
                            return 0
            
                    i = i - 1
                    j = j + 1
                
            divid = int(suma/11)
            mult = int(divid*11)
            dife = suma - mult
            digito = 11 - dife
            if digito == 10:
                    caract = "K"
        
            elif digito == 11:
                    caract = "0"
        
            else:
                    caract = str(digito).replace(" ", "")
        
            if caract == dig_rut: 
                    es_rut = True
        
            return es_rut
        
        def validate(widget):
            text = widget.get_text()
            try:
                rut_valido = not es_rut(text)
                if rut_valido :
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)
        widget.connect("focus-out-event", Format_Rut)
    def prefix_Rut(self, widget):
        self.prefix_rut(widget)
        self.add_mandatory(widget)
