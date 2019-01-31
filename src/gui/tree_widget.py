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
   from gi.repository import Gtk, Gio
   import sys
   from src import paths
   import parameters
   import resources
   import global_defines
   from parse import parse
except ImportError as err:
   print("couldn't load module. %s" % (err))
   sys.exit(2)


class tree_widget(Gtk.TreeView):

    def __init__(self):
        store = Gtk.TreeStore(str)
        store.append(None,["- no project -"])
        Gtk.TreeView.__init__(self,store)
        
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("name", renderer, text=0)
        self.append_column(column)