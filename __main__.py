#!/usr/bin/env python

import gtk
import gtksourceview2
from languages import guess_lang
import pango
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
      self._gtk.set_title("Simpleton IDE")
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
            ["Open...", lambda *_: notebook.open() ], #[ord("O"),gtk.gdk.CONTROL_MASK]],
            [],
            ["Save", lambda *_: notebook.save()],
            ["Save As", lambda *_:notebook.save_as()],
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
      self.pages = {}

   def current_page( self ):
      pagenum = self._gtk.get_current_page()
      gtk_page = self._gtk.get_nth_page(pagenum)
      return self.pages[gtk_page]

   def remove( self, page ):
      pagenum = self._gtk.page_num( page._gtk )
      self._gtk.remove_page(pagenum)
      del self.pages[page._gtk]

   def new( self, location=None ):
      def exists(loc): return\
         os.path.exists(loc) or\
         any( p.location==os.path.abspath(loc) for p in self.pages.values() ) 

      if not location:
         i = 1
         while exists("Unsaved Document %s"%i):
            i = i + 1
         location = "Unsaved Document %s"%i

      page = NotebookPage( location )
      page.x_button.bind( lambda *_: self.remove(page) )
      self._gtk.append_page( page._gtk, page._gtk_tab )
      self.pages[page._gtk] = page
      self._gtk.show_all()
      pagenum = self._gtk.page_num( page._gtk )
      self._gtk.set_current_page( pagenum )

   def open( self ):
      chooser = gtk.FileChooserDialog(title="Open a file",action=gtk.FILE_CHOOSER_ACTION_OPEN, 
         buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
      chooser.set_default_response(gtk.RESPONSE_OK)
      filter = gtk.FileFilter()
      filter.set_name("Text Files")
      filter.add_mime_type("text/data")
      filter.add_pattern("*")
      chooser.add_filter(filter)
      response = chooser.run()
      if response == gtk.RESPONSE_OK:
         notebook.new( chooser.get_filename() )
      chooser.destroy()

   def save( self ):
      page = self.current_page()
      file = open(page.location, "w")
      file.write(page.text())
      file.close()

   def save_as( self ):
      chooser = gtk.FileChooserDialog(title="Save file",action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
      chooser.set_default_response(gtk.RESPONSE_OK)
      filter = gtk.FileFilter()
      filter.set_name("Text Files")
      filter.add_mime_type("text/data")
      filter.add_pattern("*")
      chooser.add_filter(filter)
      response = chooser.run()
      if response == gtk.RESPONSE_OK:
         self.current_page().set_location( chooser.get_filename() )
         self.save()
      chooser.destroy()
      
      

class NotebookPage:
   def __init__( self, loc ):
      self._gtk_label = gtk.Label("")
      self._text_buffer = gtksourceview2.Buffer()
      self._text_buffer.set_highlight_syntax(True)
      self.set_location(loc)

      label_text = os.path.split(self.location)[1]
      if os.path.isfile(self.location):
         content_text = file(self.location).read()
      else:
         content_text = ""

      self._gtk_tab = gtk.HBox( spacing=7 )
      self._gtk_tab.add( gtk.image_new_from_icon_name("txt", 2) )
      
      self._gtk_tab.add( self._gtk_label )
      self.x_button = Button("cancel",1)
      self._gtk_tab.add( self.x_button._gtk )
      self._gtk_tab.show_all()

      

      self._text = gtksourceview2.View(self._text_buffer)
      self._text.set_show_line_numbers(True)
      self._text.set_tab_width(4)
      self._text.set_auto_indent(True)
      self._text.set_insert_spaces_instead_of_tabs(True)
      self._text.get_buffer().set_text(content_text)       
      self._text.modify_font(pango.FontDescription('monospace'))
      
      textframe = gtk.Frame()           
      textframe.set_shadow_type( gtk.SHADOW_NONE )
      textframe.add( self._text )
      self._gtk = gtk.ScrolledWindow()
      self._gtk.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
      #self._gtk.add( self._text )
      self._gtk.add_with_viewport(textframe)

   def text( self ):
      textbuffer = self._gtk_textbox.get_buffer()
      return textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())

   def set_location(self, value):
      self.location = os.path.abspath(value)
      self._gtk_label.set_text( os.path.split(self.location)[1] )
      self._text_buffer.set_language( guess_lang(self.location) )
      window._gtk.set_title("{1} ({0}) - Simpleton IDE".format(*os.path.split(self.location)) )
      
          


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










