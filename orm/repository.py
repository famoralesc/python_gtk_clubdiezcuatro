'''
Created on 20-10-2010

@author: felipe
'''
from sqlalchemy import orm, Table, MetaData, create_engine
try:
    import memcache
except ImportError:
    raise ImportError
import sys

class Beneficios(object):
    pass

class BeneficioCliente(object):
    pass

class Empresa(object):
    pass

class InstitucionEducacional(object):
    pass

class RegistroVisita(object):
    pass

class Usuarios(object):
    pass

class Clientes(object):
    visitas = orm.relationship(RegistroVisita, backref="visitas")
    

class Ciudad(object):
    pass

def make_map():
    
    db = create_engine('postgresql+psycopg2://fmorales:1020@localhost:5432/clubdiezcuatro')
    
    metadata = MetaData(db)
    beneficios_table = Table('beneficios', metadata, autoload=True)
    ben_cli_table = Table('beneficio_cliente', metadata, autoload=True)
    registro_visita_table = Table('registro_visitas', metadata, autoload=True)
    clientes_table = Table('cliente', metadata, autoload=True)
    ciudad_table = Table('ciudad', metadata, autoload=True)
    empresa_table = Table('empresa', metadata, autoload=True)
    inst_educacional_table = Table('institucion_educacional', metadata, autoload=True)
    
    usuarios_table = Table('usuarios', metadata, autoload=True)
#    cat_cli_table = Table('categoria_cliente', metadata, autoload=True)
    
    orm.mapper(Beneficios, beneficios_table)
    orm.mapper(BeneficioCliente, ben_cli_table)
    orm.mapper(Clientes, clientes_table, properties \
               = {'visitas' : orm.relationship(RegistroVisita, backref = 'visitas'),
                  'beneficios' : orm.relationship(BeneficioCliente, backref = 'beneficios')
                  })
    orm.mapper(Ciudad, ciudad_table)
    orm.mapper(Empresa, empresa_table)
    orm.mapper(InstitucionEducacional, inst_educacional_table)
    orm.mapper(RegistroVisita, registro_visita_table)
    orm.mapper(Usuarios, usuarios_table)
#    orm.mapper(CategoriaCliente, cat_cli_table)
    try:
        cliente = memcache.Client(['127.0.0.1:21201'])
        sys.__setattr__('cache', cliente)
    except:
        print "Imposible conectar con el servidor de cache"
    return db
    
    
    