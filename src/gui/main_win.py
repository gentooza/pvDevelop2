#!/usr/bin/env python3

"""
This file is part of pyPvDevelop.

Copyright 2019, Joaquín Cuéllar-

pyPvDevelop is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyPvDevelop is distributed in the hope that it will 
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyPvDevelop.  
If not, see <https://www.gnu.org/licenses/>.
"""
try:
   import gi
   gi.require_version('Gtk', '3.0')
   from gi.repository import Gtk
   import sys
   from src import paths
   import parameters
   import resources
   import global_defines
   from parse import parse
   import main_win
except ImportError as err:
   print("couldn't load module. %s" % (err))
   sys.exit(2)


class main_window(Gtk.ApplicationWindow):

    def __init__(self,app):
        my_parameters = parameters.parameters()
        if my_parameters.arg_project:
            my_title = my_parameters.arg_project + ' - Python Pvbrowser Developer'
        else:
            my_title = 'No project loaded - Python Pvbrowser Developer'
        Gtk.Window.__init__(self, title=my_title, deletable = True, application=app)
        self.set_default_icon_from_file(resources.IMG_APP_ICON)
        self.set_border_width(3)
        self.set_resizable(True)
        self.maximize()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        
        self.notebook = Gtk.Notebook()
        main_box.pack_start(self.notebook,False,False,0)

        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label('Default Page!'))
        self.notebook.append_page(self.page1, Gtk.Label('Plain Title'))

        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label('A page with an image for a Title.'))
        self.notebook.append_page(
            self.page2,
            Gtk.Image.new_from_icon_name(
                "help-about",
                Gtk.IconSize.MENU
            )
        )
        self.add(main_box)
        