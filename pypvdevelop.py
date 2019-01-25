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

"""main.py
start file
"""
try:
   import sys
   from src import paths
   import parameters, global_defines, resources, utils
   from parse import parse
   import main_win
except ImportError as err:
   print("couldn't load module. %s" % (err))
   sys.exit(2)

class py_pv_develop():
    def __init__(self):
        self.num_args = len(sys.argv)
        self.args = sys.argv
        self.parameters = parameters.parameters()
        self.parameters.initialize()
        self.get_args()
        
    def read_project(self):
        project_file_path = self.parameters.arg_project
        project_file_path += '.pvproject'
        project_file = open(project_file_path,'r')

        #previously resetting basic parameters     NO NEED
        #self.parameters.target = 'pvs'
        #self.parameters.xmax = 1280
        #self.parameters.xmax = 1024
        #self.parameters.script = 0          
        
        for line in project_file:
            if '\n' == line[-1]:
                line = line[:-1]
            if line[:7] == 'target=':
                self.parameters.target = parse("target={}",line)[0]
            elif line[:5] == 'xmax=':
                self.parameters.xmax = parse("xmax={}",line)[0]
            elif line[:5] == 'ymax=':
                self.parameters.ymax = parse("ymax={}",line)[0]
            elif line[:13] == 'script=Python':
                self.parameters.script = global_defines.PV_PYTHON
            elif line[:11] == 'script=Perl':
                self.parameters.script = global_defines.PV_PERL
            elif line[:10] == 'script=PHP':
                self.parameters.script = global_defines.PV_PHP
            elif line[:10] == 'script=Tcl':
                self.parameters.script = global_defines.PV_TCL
            elif line[:10] == 'script=Lua':
                self.parameters.script = global_defines.PV_LUA
            # add additional language here
        if(self.parameters.arg_debug):
            print('Project: target=%s xmax=%s ymax=%s script=%s\n '% (self.parameters.target, self.parameters.xmax, self.parameters.ymax, self.parameters.script))
        project_file.close()
        
    def usage(self):
        print("####################################################")
        print("# Python Develop pvserver for pvbrowser            #")
        print("####################################################")
        print("usage: pypvdevelop <-action=<action>> <-programming_language=language> <-fake_qmake> <-h> project")
        print("example: pypvdevelop pvs")
        print("example: pypvdevelop -action=writeInitialProject pvs")
        print("-action=writeInitialProject")
        print("-action=insertMask")
        print("-action=make")
        print("-action=makeModbus")
        print("-action=makeSiemensTCP")
        print("-action=makePPI")
        print("-action=uncommentRLLIB")
        print("-action=uncommentModbus")
        print("-action=uncommentSiemensTCP")
        print("-action=uncommentPPI")
        print("-action=writeStartscript")
        print("-action=writeDimension:<xmax>:<ymax>")
        print("-action=importUi:<masknumber>")
        print("-action=exportUi:<masknumber>")
        print("-action=designerUi:<masknumber>")
        print("-action=dumpTranslations")
        print("-programming_language=<Lua|Python>")
        print("- , -h, -help")
        
    def get_args(self):
        for arg in self.args:
            if arg[:6] == '-debug':
                self.parameters.arg_debug = 1
            elif arg[:8] == '-action=':
                self.parameters.arg_action = parse("-action={}",arg)[0]
            elif arg[:22] == '-programming_language=':
                buffer = parse("-programming_language={}",arg)[0]
                if(buffer == 'Python'):
                    self.parameters.script = global_defines.PV_PYTHON
                elif(buffer == 'Perl'):
                    self.parameters.script = global_defines.PV_PERL
                elif(buffer == 'PHP'):
                    self.parameters.script = global_defines.PV_PHP
                elif(buffer == 'Tcl'):
                    self.parameters.script = global_defines.PV_TCL
                elif(buffer == 'Lua'):
                    self.parameters.script = global_defines.PV_LUA
                else:
                    print("programming_language=%s not supported" % buffer)
            elif arg[:5] == '-fake':
                self.parameters.fake_qmake='-fake'
            elif (not arg.startswith('-') and (arg != './pypvdevelop.py')):
                self.parameters.arg_project = arg
                try:
                    self.parameters.arg_project = parse("{}.{}",arg)[0]
                except:
                    pass
                self.read_project()                    
            elif arg[:1] == '-' or arg[:2] == '-h' or arg[:5] == '-help':
                self.usage()
    
    def analyze_actions(self):
        if self.parameters.arg_action == '\0': #no actions provided
            return
        if self.parameters.arg_project == '\0':
            print("no project given")
            self.usage()
        utils.action(self.parameters.arg_action)
    def run(self):
        my_main_window = main_win.main_window()
        my_main_window.run()

my_app = py_pv_develop()
#not going to initialize global OPT pvbrowser tags, neither load a ini file
my_app.analyze_actions()
my_app.run()