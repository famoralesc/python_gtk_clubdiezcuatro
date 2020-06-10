'''
Created on 12-11-2010

@author: felipe
'''
USUARIOS = 1
REG_CLIENTES = 2
ASING_BENEFICIOS = 3
INSTITUCIONES = 4
BENEFICIOS = 5
ADMIN = 1000

"""
u'can_add_beneficio', u'can_add_instituciones', u'can_admin', 
u'can_asing_beneficio', u'can_manage_user', u'can_reg_cliente'
"""
def verifica_permiso(usuario, permiso):
    if usuario.can_admin:
        #Si es admin no validamos nada
        return True
        
    if permiso is USUARIOS:
        if usuario.can_manage_user:
            return True
    if permiso is BENEFICIOS:
        if usuario.can_add_beneficio:
            return True
    if permiso is INSTITUCIONES:
        if usuario.can_add_instituciones:
            return True
    if permiso is ASING_BENEFICIOS:
        if usuario.can_asing_beneficio:
            return True
    if permiso is REG_CLIENTES:
        if usuario.can_reg_cliente:
            return True
    
    return False #Siempre retornamos FALSE
    
