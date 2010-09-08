#!/usr/bin/env python

import gtk



def MainWindow():
   global window, window_vbox
   window = gtk.Window(gtk.WINDOW_TOPLEVEL)
   window.set_title("TODO set correct title - Simpleton IDE")
   window.set_default_size(1280,949)
   window.connect('destroy', gtk.main_quit)

   window_vbox = gtk.VBox()
   window.add( window_vbox )
   MenuBar()
   Toolbar()
   Notebook()
   StatusBar()
   window.show_all()
    
def MenuBar():
   global menubar
   menubar = gtk.MenuBar()
   window_vbox.pack_start( menubar, expand=False )

   def expand_menu( parent, structure ):
      for entry in structure:
         if isinstance(entry,list):
            if len(entry)==0:
               parent.append( gtk.SeparatorMenuItem() )
            else:
               item = gtk.MenuItem(entry[0])
               parent.append( item )
               if len(entry)>=2: item.connect( "activate", entry[1] )
               if len(entry)>=3: pass #todo connect accelerator
         elif isinstance(entry,tuple):
            sublabel = gtk.MenuItem(entry[0])
            submenu = gtk.Menu()
            sublabel.set_submenu(submenu)
            expand_menu( submenu, entry[1] )
            parent.append( sublabel )

   menu_structure = [
      ("File", [
         ["New"], #[ord("N"),gtk.gdk.CONTROL_MASK]],
         ["Open..."], #[ord("O"),gtk.gdk.CONTROL_MASK]],
         [],
         ["Save"],
         ["Save As"],
         ["Revert"],
         [],
         ["1. Most Recent"],
         ["2. Second Most Recent"],
         ["3. Third Most Recent"],
         ["4. Fourth Most Recent"],
         ["5. Fifth Most Recent"],
         [],
         ["Close"],
         ["Quit", gtk.main_quit],
      ]),
   ]
   expand_menu( menubar, menu_structure )
      



def Toolbar():
   global toolbar
   toolbar = gtk.Toolbar()

   go_up = gtk.Button()
   go_up.set_relief( gtk.RELIEF_NONE )
   go_up.set_focus_on_click( False ); 
   go_up.set_image( gtk.image_new_from_icon_name("stock_up", 5) )
   toolbar.append_widget( go_up, "Open the parent context", None ) 

   window_vbox.pack_start( toolbar, expand=False )
      

def Notebook():
   global notebook
   notebook = gtk.Notebook()   
   window_vbox.pack_start( notebook, expand=True )

   append_page("content 1","page 1")
   append_page("content 2","page 2")

      
def append_page( content_text, label_text ):

   #scrollable textbox
   textbox = gtk.TextView()
   textbox.get_buffer().set_text( content_text )
   textframe = gtk.Frame()           
   textframe.set_shadow_type( gtk.SHADOW_ETCHED_IN )
   textframe.add( textbox )
   sw = gtk.ScrolledWindow()
   sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
   sw.add_with_viewport(textframe)
   
   #notebook tab
   tab_hbox = gtk.HBox( spacing=7 )
   tab_hbox.add( gtk.image_new_from_icon_name("txt", 2) ) 
   tab_hbox.add( gtk.Label(label_text) )

   x_button = gtk.Button()
   x_button.set_relief( gtk.RELIEF_NONE )
   x_button.set_focus_on_click( False ); 
   x_button.set_image( gtk.image_new_from_icon_name("cancel", 1) )
   tab_hbox.add( x_button )      
   tab_hbox.show_all()
   notebook.append_page(sw,tab_hbox)



def StatusBar():
   global statusbar
   statusbar = gtk.Statusbar()   
   window_vbox.pack_start( statusbar, expand=False )
   


      






if __name__ == "__main__":
   MainWindow()
   gtk.gdk.threads_enter()
   gtk.main()
   gtk.gdk.threads_leave()










