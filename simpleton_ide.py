#!/usr/bin/env python

import gtk
import gtksourceview2
import pango
import os
import os.path
import sys
import mimetypes
import socket
import thread
import atexit
import time

#pygtk LOVES deprecation warnings
import warnings
warnings.filterwarnings("ignore")
   



lang_manager = gtksourceview2.LanguageManager()

def guess_lang( filename ):
   guess = mimetypes.guess_type(filename)
   ext = '.' + filename.split('.')[-1]
   if guess[0] in mime_to_lang: 
      return lang_manager.get_language( mime_to_lang[guess[0]] )
   elif ext in ext_to_lang:
      return lang_manager.get_language( ext_to_lang[ext] )
   else:
      return None

mime_to_lang = {
   'text/x-bibtex' : 'bibtex', 
   'text/x-boo' : 'boo', 
   'text/x-csrc' : 'c', 
   'text/x-c++src' : 'cpp', 
   'text/css' : 'css', 
   'text/x-dsrc' : 'd', 
   'text/x-diff' : 'diff', 
   'text/x-haskell' : 'haskell', 
   'text/x-literate-haskell' : 'haskell-literate', 
   'text/html' : 'html', 
   'text/x-java': 'java', 
   'text/x-tex' : 'latex', 
   'text/x-pascal' : 'pascal', 
   'text/x-perl' : 'perl', 
   'text/x-python' : 'python', 
   'text/x-sh' : 'sh', 
   'text/x-tcl' : 'tcl', 
   'text/texmacs' : 'texinfo',
}

ext_to_lang = {
   '.ada'   : 'ada',
   '.asp'   : 'asp', 
   '.awk'   : 'awk', 
   '.bib'   : 'bibtex',
   '.cs'    : 'c-sharp', 
   '.cg'    : 'cg', 
   '.cmake' : 'cmake', 
   '.cuda'  : 'cuda', 
   '.bat'   : 'dosbatch', 
   '.e'     : 'eiffel', 
   '.erl'   : 'erlang', 
   '.f'     : 'fortran',
   '.for'   : 'fortran',
   '.f90'   : 'fortran',
   '.f95'   : 'fortran', 
   '.fs'    : 'fsharp', 
   '.js'    : 'js', 
   '.lua'   : 'lua', 
   '.m4'    : 'm4', 
   '.make'  : 'makefile', 
   '.page'  : 'mallard', 
   '.msil'  : 'msil', 
   '.n'     : 'nemerle', 
   '.m'     : 'objc', 
   '.ml'    : 'objective-caml', 
   '.ocl'   : 'ocl', 
   '.m'     : 'octave', 
   '.ooc'   : 'ooc', 
   '.php'   : 'php', 
   '.r'     : 'r', 
   '.rb'    : 'ruby', 
   '.scala' : 'scala',
   '.ss'    : 'scheme', 
   '.sql'   : 'sql', 
   '.vb'    : 'vbnet', 
   '.xml'   : 'xml', 
   '.y'     : 'yacc',
}


def icon( icon_name, icon_size ):
   return gtk.image_new_from_icon_name(icon_name,icon_size)

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
         
   #check to make sure that only one instance is running
   FILE = "\0simpleton_ide"   
   try:     
      s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
      s.bind(FILE)
      def ipc():      
         while True:
            notebook.new( s.recvfrom(1024)[0] )
      thread.start_new_thread( ipc, () )    
   except socket.error, E:
      print 'primary, socket.error', E
      try:
         for loc in sys.argv[1:]:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            s.sendto(loc,FILE)
            s.close()
      except socket.error, E:
         print 'secondary, socket.error', E
      sys.exit(0)
    

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
         ("Edit", [
            ["Find...", lambda *_: notebook.do_search()],
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

      self._gtk.append_item(None, "Create a new document", None, icon("document-new", 3) , lambda *_:notebook.new())
      self._gtk.append_item("Open", "Open a file", None, icon("document-open", 3) , lambda *_:notebook.open())
      self._gtk.append_item("Save", "Save the current file", None, icon("document-save", 3) , lambda *_:notebook.save())

      

class Notebook:
   def __init__( self ):
      self._gtk = gtk.Notebook()   
      self.pages = {}
      window._gtk.connect("key_press_event",lambda *_:self.update_label())
      window._gtk.connect("set-focus",lambda *_:self.update_label())

      
   def update_label( self ):
      self.current_page() and self.current_page().update_label()

   def current_page( self ):
      pagenum = self._gtk.get_current_page()
      gtk_page = self._gtk.get_nth_page(pagenum)
      return gtk_page and gtk_page in self.pages and self.pages[gtk_page]

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
      page._text_buffer.set_modified(False)
      self.update_label()

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
      
   def search_callback(self, dialog, response_id):
      if response_id == -1:
         dialog.destroy()
         return

      start, end = dialog.buffer.get_bounds()
      search_string = start.get_text(end)

      self.search(search_string, forward=True)

   def do_search(self):
      search_text = gtk.TextView()
      dialog = gtk.Dialog("Find", window._gtk,
                         gtk.DIALOG_DESTROY_WITH_PARENT,
                         ("Close", -1,
                          "Find", 0 ) )
      dialog.vbox.pack_end(search_text, True, True, 0)
      dialog.buffer = search_text.get_buffer()
      dialog.connect("response", self.search_callback)

      search_text.show()
      search_text.grab_focus()
      dialog.show_all()
      
   def search(self, str, forward):
      page = self.current_page()
      buffer = page._text_buffer
      start, end = buffer.get_bounds()
      buffer.remove_tag(page.found_text_tag, start, end)

      iter = buffer.get_start_iter()

      while str:
         res = iter.forward_search(str, gtk.TEXT_SEARCH_TEXT_ONLY)
         #res = iter.backward_search(str, gtk.TEXT_SEARCH_TEXT_ONLY)
         if not res:
            break
         match_start, match_end = res
         buffer.apply_tag(page.found_text_tag, match_start, match_end)
         iter = match_end

      
      

class NotebookPage:
   def __init__( self, loc ):
      
      self._gtk_label = gtk.Label("")
      self._gtk_tab = gtk.HBox( spacing=7 )
      self._gtk_tab.add( gtk.image_new_from_icon_name("txt", 2) )
      
      self._gtk_tab.add( self._gtk_label )
      self.x_button = Button("cancel",1)
      self._gtk_tab.add( self.x_button._gtk )
      self._gtk_tab.show_all()

      self._text_buffer = gtksourceview2.Buffer()
      self._text_buffer.set_highlight_matching_brackets(False)
      self._text_buffer.set_highlight_syntax(True)
      self.found_text_tag = self._text_buffer.create_tag(background="yellow")
      self._text = gtksourceview2.View(self._text_buffer)
      #self._text.set_show_line_numbers(True)
      self._text.set_tab_width(3)
      self._text.set_auto_indent(True)
      self._text.set_insert_spaces_instead_of_tabs(True)
      
      self._text.modify_font(pango.FontDescription('monospace'))
      
      textframe = gtk.Frame()           
      textframe.set_shadow_type( gtk.SHADOW_NONE )
      textframe.add( self._text )
      self._gtk = gtk.ScrolledWindow()
      self._gtk.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
      self._gtk.add_with_viewport(textframe)

      self.set_location(loc)
      if os.path.isfile(self.location):
         content_text = file(self.location).read()
      else:
         content_text = ""
      self._text_buffer.begin_not_undoable_action()
      self._text_buffer.set_text(content_text)  
      self._text_buffer.end_not_undoable_action()   
      self._text_buffer.set_modified(False)
      
   def text( self ):
      buff = self._text_buffer
      return buff.get_text(buff.get_start_iter() , buff.get_end_iter())

   def set_location(self, value):
      self.location = os.path.abspath(value)
      self._text_buffer.set_language( guess_lang(self.location) )
      self.update_label()

   def update_label( self ):
      modmark = self._text_buffer.get_modified() and '*' or ''
      self._gtk_label.set_text( modmark + os.path.split(self.location)[1] )
      window._gtk.set_title( modmark + "{1} ({0}) - Simpleton IDE".format(*os.path.split(self.location)) )
      
          


class Button:
   def __init__( self, icon_name, icon_size ):
      self._gtk = gtk.Button()
      self._gtk.set_image( gtk.image_new_from_icon_name( icon_name, icon_size ) )
      #icon = gtk.icon_theme_get_default().load_icon( "stock_up", 5, () )
      self._gtk.set_relief( gtk.RELIEF_NONE )
      self._gtk.set_focus_on_click( False )
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










