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

"""utils.py - base generic functions.
based on pvdevelop cutils
"""
try:
   import subprocess
   import sys
   from pathlib import Path
   from src import paths
   import parameters, global_defines, resources
   from parse import parse
   import main_win
except ImportError as err:
   print("couldn't load module. %s" % (err))
   sys.exit(2)

def my_system(command):
    my_command_list = command.split()
    subprocess.Popen(my_command_list)
    #my_process.wait ?

def action(command):
    if(len(command) > (1024-80)):
        print("You silly stupid DAU. Why use such a long name ???")
        print(command)
    my_parameters = parameters.parameters()
    if my_parameters.arg_debug:
        print("action(%s)"%command)
    #qmake
    if command[:6] == 'qmake=' and my_parameters.script != global_defines.PV_LUA:
        project = parse("qmake={}",command)[0]
        new_command = 'fake_qmake ' + str(my_parameters.fake_qmake) + ' ' + project + '.pro'
        if my_parameters.arg_debug:
            print(" executing: %s"%new_command)
        my_system(new_command)  
    #insertMask
    elif command[:11] == 'insertMask=':
        extension='.cpp'
        if my_parameters.script == global_defines.PV_LUA:
            extension = '.lua'
            
        project = parse("insertMask={}",command)[0]
        project += '.pro'

        file = 'mask{0}' + extension
        index = 1
        while Path(file.format(str(index))).exists():
            index +=1
        print('create file number %d'% index)        

    else:
        print("%s not implemented yet" % command)

