#!/usr/bin/env python

import gtk


class MenuBar:
   def __init__( self, parent ):
      self.parent = parent
      self.menubar = gtk.MenuBar()
      self.parent.pack_start( self.menubar, expand=False )

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

      self.expand_menu( self.menubar, menu_structure )
      

   def expand_menu( self, parent, structure ):
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
            self.expand_menu( submenu, entry[1] )
            parent.append( sublabel )

      

class Notebook:

   def __init__( self, parent ):
      self.parent = parent
      self.notebook = gtk.Notebook()   

      self.append_page("content 1","page 1")
      self.append_page("content 2","page 2")

      self.parent.pack_start( self.notebook, expand=True )

   def append_page( self, content_text, label_text ):

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
      tab_hbox.add( gtk.image_new_from_icon_name("stock_close", 1) )      
      tab_hbox.show_all()
      self.notebook.append_page(sw,tab_hbox)



class StatusBar:
   def __init__( self, parent ):
      self.parent = parent
      self.statusbar = gtk.Statusbar()   
      self.parent.pack_start( self.statusbar, expand=False )
   


class MainWindow:
   def __init__( self ):

      self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
      self.window.set_title("TODO set correct title - Simpleton IDE")
      self.window.set_default_size(1280,949)
      self.window.connect('destroy', gtk.main_quit)

      self.vbox = gtk.VBox()
      self.window.add( self.vbox )
      MenuBar( self.vbox )
      Notebook( self.vbox )
      StatusBar( self.vbox )
      
      self.window.show_all()





if __name__ == "__main__":
   MainWindow()
   gtk.gdk.threads_enter()
   gtk.main()
   gtk.gdk.threads_leave()










