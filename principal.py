from frm_principal import Principal
from orm.repository import make_map
import gtk

if __name__ == "__main__":
    db = make_map()
    principal = Principal(cnx = db)
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    gtk.main()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    