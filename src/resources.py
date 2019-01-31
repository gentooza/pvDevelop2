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

"""resources.py - images path and resources.
"""
import sys
import os
try:
   import gi
   gi.require_version('Gtk', '3.0')
   from gi.repository import Gtk, Gdk, Gio
   from src import paths
except ImportError as err:
   print("couldn't load module. %s" % (err))
   sys.exit(2)


ICONS_FOLDER = Gio.File.new_for_path(paths.abs_progdir+'/images/')

# add additional language here
IMG_APP_ICON = paths.abs_progdir+'/images/app.png'
#menu icons

ICON_OPTIONS = Gio.FileIcon.new(ICONS_FOLDER.get_child('option.png'))
#ICON_OPTIONS = ICON_OPTIONS_.serialize()
#menu_xml_GTK_descriptors
UI_MAIN_MENU = paths.abs_progdir+'/src/gui/main_menu.ui'



