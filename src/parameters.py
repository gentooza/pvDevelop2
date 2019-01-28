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

"""parameters.py - global app parameters.
Borg pattern used, ref: http://code.activestate.com/recipes/66531-singleton-we-dont-need-no-stinkin-singleton-the-bo/
"""

try:
   import  global_defines
except ImportError as err:
   print("couldn't load module. %s" % (err))
   sys.exit(2)

class parameters:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        
    def initialize(self):
        #hardcoded as in the original
        self.x_grid = self.y_grid = 3 # default grid for designer
        self.murx = 0 # default option for testing pvdevelop
        self.ctrl_pressed = 0
        self.su = 1 # run pvs as root
        self.xmax = 1280 # default dimension for designer
        self.ymax = 1024
        self.backup_location = '..'
        self.arg_debug = 0
        self.arg_action = '\0'
        self.script = 0
        self.arg_mask_to_generate = -1
        self.arg_project = ''
        self.manual = '/opt/pvb/doc/index.html'
        self.fake_qmake = ''
        self.target = ''
        #communications
        self.port=5050
        self.sshport=50500
        self.autoreconnect=0
        self.ssh=''
        self.initialhost=''
        #pvbrowser visualization
        self.zoom=100
        self.fontzoom=100
        self.menubar=1
        self.toolbar=1
        self.statusbar=1
        self.scrollbars=1
        self.fullscreen=0
        self.maximized=0
        self.tabs_above_toolbar=0
        self.echo_table_updates=0
        self.customlogo = ''
        #behaviour
        self.newwindow=''
        self.exitpassword=0
        self.view_audio=''
        self.view_video=''
        self.view_pdf=''
        self.view_img=''
        self.view_svg=''
        self.view_txt=''
        self.view_html=''
        self.language=''
        self.codec=pvbUTF8
        #QT and versions
        self.QT_version = 0x040601
        self.use_webkit_for_svg=1
         #misc      
        self.temp = ''
        self.i_have_started_servers=0
        self.closed=0
        self.cookies=0
        self.manual='index.html'