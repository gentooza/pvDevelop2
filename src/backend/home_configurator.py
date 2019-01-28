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
   import re
   import subprocess
   import datetime
   import sys
   from pathlib import Path
   from src import paths
   import parameters, global_defines, resources
   from parse import parse
except ImportError as err:
   print("couldn't load module. %s" % (err))
   sys.exit(2)



def check_and_create_home():
    my_parameters = parameters.parameters()
    home_dir = str(Path.home())
    home_dir = home_dir + '/.pypvbrowser'
    
    home_dir_path = Path(home_dir)
    if home_dir_path.exists():
        if my_parameters.arg_debug:
            print('home folder exists!')
    else:
        home_dir_path.mkdir(parents=True, exist_ok=True)
        
    check_and_create_ini()        
    
 
def check_and_create_ini():
    my_parameters = parameters.parameters()   
    ini_file = str(Path.home())
    ini_file = ini_file + '/.pypvbrowser/configuration'
    
    ini_file_path = Path(ini_file)
    if ini_file_path.exists():
        if my_parameters.arg_debug:
            print('ini file exists!')
        with  open(ini_file,'r')  as ini_file_handler:
            file_content = ini_file_handler.readlines()
            for line in file_content:
                
                if re.search('manual=',line):
                    try:
                        my_parameters.manual= parse('manual={}',line)[0]
                    except:
                        pass
                    
                if re.search('xGrid=',line):
                    try:
                        my_parameters.x_grid= int(parse('xGrid={}',line)[0])
                        if my_parameters.x_grid<=0:
                            my_parameters.x_grid=1
                    except:
                        pass
  
                if re.search('yGrid=',line):
                    try:
                        my_parameters.y_grid= int(parse('yGrid={}',line)[0])
                        if my_parameters.y_grid<=0:
                            my_parameters.y_grid=1   
                    except:
                        pass
                
                if re.search('su=',line):
                    try:
                        my_parameters.su= int(parse('su={}',line)[0])
                    except:
                        pass
                    
                if re.search('backupLocation=',line):
                    try:
                        my_parameters.backup_location=parse('backupLocation={}',line)[0]
                    except:
                        pass
                
    else:
        lines_to_write =['xGrid=3\n',
                     'yGrid=3\n',
                     'manual=/opt/pvb/doc/index.html\n',
                     '# run pvs as root 0|1\n',
                     'su=0',
                     'backupLocation=..\n'
                     ]
        with  open(ini_file,'w')  as ini_file_handler:
            ini_file_handler.writelines(lines_to_write) 
                     
    