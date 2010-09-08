#!/usr/bin/env python

import gtk



def main():
   global window
   window = Window()
   window.add( Menubar(),     expand=False   )
   window.add( Toolbar(),     expand=False   )
   window.add( Notebook(),    expand=True    )
   window.add( Statusbar(),   expand=False   )
    

class Window:
   def __init__( self ):
      self._gtk = gtk.Window( gtk.WINDOW_TOPLEVEL )
      self._gtk.set_title("TODO set correct title - Simpleton IDE")
      self._gtk.set_default_size(1280,949)
      self._gtk.connect('destroy', gtk.main_quit)

      self._vbox = gtk.VBox()
      self._gtk.add( self._vbox )
      self._gtk.show_all()

   def add( self, widget, expand=True ):
      self._vbox.pack_start( widget._gtk, expand )
      widget._gtk.show_all()


class Menubar:
   def __init__( self ):
      self._gtk = gtk.MenuBar()
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
      self.expand_menu( self._gtk, menu_structure )

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

   
      


class Toolbar:
   def __init__( self ):
      self._gtk = gtk.Toolbar()

      go_up = gtk.Button()
      go_up.set_relief( gtk.RELIEF_NONE )
      go_up.set_focus_on_click( False ); 
      go_up.set_image( gtk.image_new_from_icon_name("stock_up", 5) )
      self._gtk.append_widget( go_up, "Open the parent context", None ) 
      

class Notebook:
   def __init__( self ):
      self._gtk = gtk.Notebook()   
      self.append_page("content 1","page 1")
      self.append_page("content 2","page 2")
      
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

      x_button = gtk.Button()
      x_button.set_relief( gtk.RELIEF_NONE )
      x_button.set_focus_on_click( False ); 
      x_button.set_image( gtk.image_new_from_icon_name("cancel", 1) )
      tab_hbox.add( x_button )      
      tab_hbox.show_all()
      self._gtk.append_page(sw,tab_hbox)



class Statusbar:
   def __init__( self ):
      self._gtk = gtk.Statusbar()   
   


      






if __name__ == "__main__":
   main()
   gtk.gdk.threads_enter()
   gtk.main()
   gtk.gdk.threads_leave()










