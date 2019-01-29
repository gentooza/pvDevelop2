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
   from gi.repository import Gtk, Gdk
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


class main_menu(Gtk.UIManager):
    UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='FileOptions' />
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='EditMenu'>
      <menuitem action='EditCopy' />
      <menuitem action='EditPaste' />
      <menuitem action='EditSomething' />
    </menu>
    <menu action='ChoicesMenu'>
      <menuitem action='ChoiceOne'/>
      <menuitem action='ChoiceTwo'/>
      <separator />
      <menuitem action='ChoiceThree'/>
    </menu>
  </menubar>
  <toolbar name='ToolBar'>
    <toolitem action='FileNewStandard' />
    <toolitem action='FileQuit' />
  </toolbar>
  <popup name='PopupMenu'>
    <menuitem action='EditCopy' />
    <menuitem action='EditPaste' />
    <menuitem action='EditSomething' />
  </popup>
</ui>
"""
    def __init__(self,parent):
        Gtk.UIManager.__init__(self)
        
        # Throws exception if something went wrong
        self.add_ui_from_string(self.UI_INFO)

        # Add the accelerator group to the toplevel window
        accelgroup = self.get_accel_group()
        parent.add_accel_group(accelgroup)
        
    def set_actions(self,parent_window):
        action_group = Gtk.ActionGroup("my_actions")
     
        self.add_file_menu_actions(action_group, parent_window)
        self.add_edit_menu_actions(action_group, parent_window)
        self.add_choices_menu_actions(action_group, parent_window)  
        
        self.insert_action_group(action_group)
        
    def add_file_menu_actions(self, action_group, parent_window):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_file_options = Gtk.Action("FileOptions", "Options", None, None)
        action_file_options.connect("activate", parent_window.on_menu_file_quit)
        action_group.add_action(action_file_options)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", parent_window.on_menu_file_quit)
        action_group.add_action(action_filequit)

    def add_edit_menu_actions(self, action_group, parent_window):
        action_group.add_actions([
            ("EditMenu", None, "Edit"),
            ("EditCopy", Gtk.STOCK_COPY, None, None, None,
             parent_window.on_menu_others),
            ("EditPaste", Gtk.STOCK_PASTE, None, None, None,
             parent_window.on_menu_others),
            ("EditSomething", None, "Something", "<control><alt>S", None,
             parent_window.on_menu_others)
        ])

    def add_choices_menu_actions(self, action_group, parent_window):
        action_group.add_action(Gtk.Action("ChoicesMenu", "Choices", None,
            None))

        action_group.add_radio_actions([
            ("ChoiceOne", None, "One", None, None, 1),
            ("ChoiceTwo", None, "Two", None, None, 2)
        ], 1, parent_window.on_menu_choices_changed)

        three = Gtk.ToggleAction("ChoiceThree", "Three", None, None)
        three.connect("toggled", parent_window.on_menu_choices_toggled)
        action_group.add_action(three)
