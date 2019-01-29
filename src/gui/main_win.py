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
   import main_menu
except ImportError as err:
   print("couldn't load module. %s" % (err))
   sys.exit(2)


class main_window(Gtk.Window):

    def __init__(self):
        my_parameters = parameters.parameters()
        if my_parameters.arg_project:
            my_title = my_parameters.arg_project + ' - Python Pvbrowser Developer'
        else:
            my_title = 'No project loaded - Python Pvbrowser Developer'
        Gtk.Window.__init__(self, title=my_title, deletable = True)
        self.set_default_icon_from_file(resources.IMG_APP_ICON)
        self.set_border_width(3)
        self.set_resizable(True)
        self.maximize()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        #menu
        self.ui_manager = main_menu.main_menu(self)
        menu_bar = self.ui_manager.get_widget("/MenuBar")
        self.ui_manager.set_actions(self)
        main_box.pack_start(menu_bar,False,False,0)
        
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
        
    def on_menu_file_new_generic(self, widget):
        print("A File|New menu item was selected.")

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()

    def on_menu_others(self, widget):
        print("Menu item " + widget.get_name() + " was selected")

    def on_menu_choices_changed(self, widget, current):
        print(current.get_name() + " was selected.")

    def on_menu_choices_toggled(self, widget):
        if widget.get_active():
            print(widget.get_name() + " activated")
        else:
            print(widget.get_name() + " deactivated")


    def run(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()