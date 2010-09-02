#!/usr/bin/env python

import gtk

class Notebook:

   def __init__( self, parent ):
      self.parent = parent
      self.notebook = gtk.Notebook()   
      self.notebook.show()   

      self.append_page("content 1","page 1")
      self.append_page("content 2","page 2")

      self.parent.add( self.notebook )
      

   def append_page( self, content_text, label_text ):

      #content
      frame = gtk.Frame()
      frame.show()

      #label
      hbox = gtk.HBox( spacing=7 )

      hbox_icon = gtk.image_new_from_icon_name("txt", 2)
      hbox_icon.show()
      hbox.add( hbox_icon ) 

      hbox_label = gtk.Label(label_text)
      hbox_label.show()
      hbox.add( hbox_label )

      hbox_close = gtk.image_new_from_icon_name("stock_close", 1)
      hbox_close.show()
      hbox.add( hbox_close )      

      self.notebook.append_page(frame,hbox)

   

class MainWindow:
   def __init__( self ):

      self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
      self.window.set_title("TODO set correct title - Simpleton IDE")
      self.window.set_default_size(1280,949)
      self.window.connect('destroy', gtk.main_quit)
      self.window.show()

      Notebook( self.window )
   


if __name__ == "__main__":
   MainWindow()
   gtk.gdk.threads_enter()
   gtk.main()
   gtk.gdk.threads_leave()










