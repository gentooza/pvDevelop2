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
        self.arg_project = 'pvs'
        self.manual = '/opt/pvb/doc/index.html'
        self.fake_qmake = ''

