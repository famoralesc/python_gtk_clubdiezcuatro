#!/usr/bin/env python
# -*- coding: UTF8 -*-
'''
Created on 19-10-2010

@author: felipe
'''
import os, gtk
import sys
path= os.getcwd()
print path
path2 = os.sep.join(path.split(os.sep) + ['lib-dev'])
sys.path.insert(0,'%s'%path2)
path2 = os.sep.join(path.split(os.sep) + ['widgets'])
sys.path.insert(0,'%s'%path2)
#path2 = os.sep.join(path.split(os.sep) + ['scp'])
#sys.path.insert(0,'%s'%path2)
#path2 = os.sep.join(path.split(os.sep) + ['scp', 'public'])
#sys.path.insert(0,'%s'%path2)
#path2 = os.sep.join(path.split(os.sep) + ['orm'])
#sys.path.insert(0,'%s'%path2)
path2 = os.sep.join(path.split(os.sep) + ['orm', 'gsa'])
sys.path.insert(0,'%s'%path2)
path2 = os.sep.join(path.split(os.sep) + ['orm', 'gsa', 'cc'])
sys.path.insert(0,'%s'%path2)
path2 = os.sep.join(path.split(os.sep) + ['orm', 'gsa', 'comun'])
sys.path.insert(0,'%s'%path2)
path2 = os.sep.join(path.split(os.sep) + ['orm', 'gsa', 'postventa'])
sys.path.insert(0,'%s'%path2)
path2 = os.sep.join(path.split(os.sep) + ['orm', 'gsa', 'public'])
sys.path.insert(0,'%s'%path2)



#path2 = os.sep.join(path.split(os.sep) + ['orm','scc'])
sys.path.insert(0,'%s'%path2)
#path2 = os.sep.join(path.split(os.sep) + ['orm','scc','cc'])
sys.path.insert(0,'%s'%path2)
#path2 = os.sep.join(path.split(os.sep) + ['orm','scc','postventa'])
sys.path.insert(0,'%s'%path2)
#path2 = os.sep.join(path.split(os.sep) + ['scp', 'bdg'])
sys.path.insert(0,'%s'%path2)
#path2 = os.sep.join(path.split(os.sep) + ['orm','common_services'])
sys.path.insert(0,'%s'%path2)
path2 = os.sep.join(path.split(os.sep) + ['custom_services'])
sys.path.insert(0,'%s'%path2)
path2 = os.sep.join(path.split(os.sep) + ['common_services'])
sys.path.insert(0,'%s'%path2)


#print(sys.path)
#from ventas import *
from libdev.SimpleGladeApp import SimpleGladeApp
from libdev import SimpleTree
#from comunes import *
from libdev.dialogos import *
import datetime
from libdev.GladeConnect import GladeConnect
#from completions import *
#import spg as psycopg
from libdev.coneccion import dlgConeccion, dlgSeleccionEmpresa
import libdev.debugwindow
from sqlalchemy import orm, Table, MetaData
import permisos
PORC_IVA = 19.0