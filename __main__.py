#!/usr/bin/env python

import gtk
import os.path
import sys


def main():
   global window, notebook
   window = Window(); notebook = Notebook()
   window.add( Menubar(),     expand=False   )
   window.add( Toolbar(),     expand=False   )
   window.add( notebook,      expand=True    )
   window.add( Statusbar(),   expand=False   )

   if len(sys.argv)==1: 
      notebook.new()
   else:
      for loc in sys.argv[1:]:
         notebook.new( loc )
    

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
            ["New", lambda *_: notebook.new()], #[ord("N"),gtk.gdk.CONTROL_MASK]],
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
      go_up = Button("stock_up", 5)
      self._gtk.append_widget( go_up._gtk, "Open the parent context", None ) 
      

class Notebook:
   def __init__( self ):
      self._gtk = gtk.Notebook()   
      self.pages = set()

   def remove( self, page ):
      pagenum = self._gtk.page_num( page._gtk )
      self._gtk.remove_page(pagenum)
      self.pages.remove(page)

   def new( self, location=None ):
      def exists(loc): return\
         os.path.exists(loc) or\
         any( p.location==os.path.abspath(loc) for p in self.pages ) 

      if not location:
         i = 1
         while exists("Unsaved Document %s"%i):
            i = i + 1
         location = "Unsaved Document %s"%i

      page = NotebookPage( location )
      page.x_button.bind( lambda *_: self.remove(page) )
      self._gtk.append_page( page._gtk, page._gtk_tab )
      self.pages.add( page )
      self._gtk.show_all()
      

class NotebookPage:
   def __init__( self, location ):
      self.location = os.path.abspath(location)
      label_text = os.path.split(location)[1]
      if os.path.isfile(location):
         content_text = file(location).read()
      else:
         content_text = ""

      self._gtk_tab = gtk.HBox( spacing=7 )
      self._gtk_tab.add( gtk.image_new_from_icon_name("txt", 2) )
      self._gtk_tab.add( gtk.Label( label_text ) )
      self.x_button = Button("cancel",1)
      self._gtk_tab.add( self.x_button._gtk )
      self._gtk_tab.show_all()

      textbox = gtk.TextView()
      textbox.get_buffer().set_text( content_text )
      textframe = gtk.Frame()           
      textframe.set_shadow_type( gtk.SHADOW_ETCHED_IN )
      textframe.add( textbox )
      self._gtk = gtk.ScrolledWindow()
      self._gtk.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
      self._gtk.add_with_viewport(textframe)


class Button:
   def __init__( self, icon_name, icon_size ):
      self._gtk = gtk.Button()
      self._gtk.set_relief( gtk.RELIEF_NONE )
      self._gtk.set_focus_on_click( False )
      self._gtk.set_image( gtk.image_new_from_icon_name( icon_name, icon_size ) )
      self._gtk.show_all()
   def bind( self, event ):
      self._gtk.connect('button_release_event', event)


class Statusbar:
   def __init__( self ):
      self._gtk = gtk.Statusbar()   
   


      






if __name__ == "__main__":
   main()
   gtk.gdk.threads_enter()
   gtk.main()
   gtk.gdk.threads_leave()










