#!/usr/bin/env python

import sys
import gtk

Window = gtk.Window(gtk.WINDOW_TOPLEVEL)
Window.set_title("TODO set correct title - Simpleton IDE")
Window.set_default_size(1280,949)
Window.connect('destroy', gtk.main_quit)
Window.show_all()

if __name__ == "__main__":
   gtk.gdk.threads_enter()
   gtk.main()
   gtk.gdk.threads_leave()






