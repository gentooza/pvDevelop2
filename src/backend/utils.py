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
        file = file.format(index)
        generate_initial_mask(index)
        generate_initial_slots(index)
        if my_parameters.script != global_defines.PV_LUA:
            add_mask_to_project(project,index) #add masks to project.pro QMAKE file
        add_mask_to_main(index)
        if my_parameters.script != global_defines.PV_LUA:
            add_mask_to_header(index)
    #make

    else:
        print("%s not implemented yet" % command)


def generate_initial_mask(index):
    my_parameters = parameters.parameters()
    #TODO: different languages by plugins!
    if my_parameters.script == global_defines.PV_LUA:
        lua_generate_initial_mask(index)
    else: #C++
        cpp_generate_initial_mask(index)
                        
def lua_generate_initial_mask(index):
    print('LUA not implemented yet!')
    
def cpp_generate_initial_mask(index):
    mask_file = 'mask{0}.cpp' 
    mask_file = mask_file.format(index)
    mask_name = parse('{}.cpp',mask_file)[0]
    #TODO: add license notice here!
    lines_to_write =['////////////////////////////////////////////////////////////////////////////\n',
                     '//\n',
                     '// show_{file_name} for ProcessViewServer created: {creation_date}\n'.format(file_name=mask_file,creation_date=datetime.datetime.now().strftime("%I:%M%p // %Y/%B/%d")),
                     '//\n',
                     '////////////////////////////////////////////////////////////////////////////\n',
                     '#include \"pvapp.h\"\n',
                     '// _begin_of_generated_area_ (do not edit -> use ui2pvc) -------------------\n',
                     '\n',
                     '// our mask contains the following objects\n',
                     'enum {\n'
                     '  ID_MAIN_WIDGET = 0,\n',
                     '  ID_END_OF_WIDGETS\n',
                     '};\n',
                     '\n',
                     'static const char *toolTip[] = {\n',
                     '  \"\"\n',
                     '};\n',
                     '\n',
                     'static const char *whatsThis[] = {\n',
                     '  \"\"\n',
                     '};\n',
                     '\n',
                     'static int generated_defineMask(PARAM *p)\n',
                     '{\n',
                     '  int w,h,depth;\n',
                     '\n',
                     '  if(p == NULL) return 1;\n',
                     '  w = h = depth = strcmp(toolTip[0],whatsThis[0]);\n',
                     '  if(w==h) depth=0; // fool the compiler\n',
                     '  pvStartDefinition(p,ID_END_OF_WIDGETS);\n',
                     '  pvEndDefinition(p);\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     '// _end_of_generated_area_ (do not edit -> use ui2pvc) ---------------------\n',
                     '\n',
                     '#include \"{}_slots.h\"\n'.format(mask_name),
                     '\n',
                     'static int defineMask(PARAM *p)\n',
                     '{\n',
                     '  if(p == NULL) return 1;\n',
                     '  generated_defineMask(p);\n',
                     '  // (todo: add your code here)\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     '\n',
                     'static int showData(PARAM *p, DATA *d)\n',
                     '{\n',
                     '  if(p == NULL) return 1;\n',
                     '  if(d == NULL) return 1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int readData(DATA *d) // from shared memory, database or something else\n',
                     '{\n',
                     '  if(d == NULL) return 1;\n',
                     '  // (todo: add your code here)\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     '\n',
                     'int show_{}(PARAM *p)\n'.format(mask_name),
                     '{\n',
                     '  DATA d;\n',
                     '  char event[MAX_EVENT_LENGTH];\n',
                     '  char text[MAX_EVENT_LENGTH];\n',
                     '  char str1[MAX_EVENT_LENGTH];\n',
                     '  int  i,w,h,val,x,y,button,ret;\n',
                     '  float xval, yval;\n',
                     '\n',
                     '  defineMask(p);\n',
                     '  //rlSetDebugPrintf(1);\n',
                     '  if((ret=slotInit(p,&d)) != 0) return ret;\n',
                     '  readData(&d); // from shared memory, database or something else\n',
                     '  showData(p,&d);\n',
                     '  pvClearMessageQueue(p);\n',
                     '  while(1)\n',
                     '  {\n',
                     '    pvPollEvent(p,event);\n',
                     '    switch(pvParseEvent(event, &i, text))\n'
                     '  {\n',
                     '      case NULL_EVENT:\n',
                     '        readData(&d); // from shared memory, database or something else\n',
                     '        showData(p,&d);\n',
                     '        if((ret=slotNullEvent(p,&d)) != 0) return ret;\n',
                     '        break;\n',
                     '      case BUTTON_EVENT:\n',
                     '        if(trace) printf(\"BUTTON_EVENT id=%d\\n\",i);\n',
                     '        if((ret=slotButtonEvent(p,i,&d)) != 0) return ret;\n',
                     '        break;\n',
                     '      case BUTTON_PRESSED_EVENT:\n',
                     '        if(trace) printf(\"BUTTON_PRESSED_EVENT id=%d\\n\",i);\n',
                     '        if((ret=slotButtonPressedEvent(p,i,&d)) != 0) return ret;\n',
                     '        break;\n',
                     '      case BUTTON_RELEASED_EVENT:\n',
                     '        if(trace) printf(\"BUTTON_RELEASED_EVENT id=%d\\n\",i);\n',
                     '        if((ret=slotButtonReleasedEvent(p,i,&d)) != 0) return ret;\n',
                     '        break;\n',
                     '      case TEXT_EVENT:\n',
                     '        if(trace) printf(\"TEXT_EVENT id=%d %s\\n\",i,text);\n',
                     '        if((ret=slotTextEvent(p,i,&d,text)) != 0) return ret;\n',
                     '        break;\n',
                     '      case SLIDER_EVENT:\n',
                     '        sscanf(text,\"(%d)\",&val);\n',
                     '        if(trace) printf(\"SLIDER_EVENT val=%d\\n\",val);\n',
                     '        if((ret=slotSliderEvent(p,i,&d,val)) != 0) return ret;\n',
                     '        break;\n',
                     '      case CHECKBOX_EVENT:\n',
                     '        if(trace) printf(\"CHECKBOX_EVENT id=%d %s\\n\",i,text);\n',
                     '        if((ret=slotCheckboxEvent(p,i,&d,text)) != 0) return ret;\n',
                     '        break;\n',
                     '      case RADIOBUTTON_EVENT:\n',
                     '        if(trace) printf(\"RADIOBUTTON_EVENT id=%d %s\\n\",i,text);\n',
                     '        if((ret=slotRadioButtonEvent(p,i,&d,text)) != 0) return ret;\n',
                     '        break;\n',
                     '      case GL_INITIALIZE_EVENT:\n',
                     '        if(trace) printf(\"you have to call initializeGL()\\n\");\n',
                     '        if((ret=slotGlInitializeEvent(p,i,&d)) != 0) return ret;\n',
                     '        break;\n',
                     '      case GL_PAINT_EVENT:\n',
                     '        if(trace) printf(\"you have to call paintGL()\\n\");\n',
                     '        if((ret=slotGlPaintEvent(p,i,&d)) != 0) return ret;\n',
                     '        break;\n',
                     '      case GL_RESIZE_EVENT:\n',
                     '        sscanf(text,\"(%d,%d)\",&w,&h);\n',
                     '        if(trace) printf(\"you have to call resizeGL(w,h)\\n\");\n',
                     '        if((ret=slotGlResizeEvent(p,i,&d,w,h)) != 0) return ret;\n',
                     '        break;\n',
                     '      case GL_IDLE_EVENT:\n',
                     '        if((ret=slotGlIdleEvent(p,i,&d)) != 0) return ret;\n',
                     '        break;\n',
                     '      case TAB_EVENT:\n',
                     '        sscanf(text,\"(%d)\",&val);\n',
                     '        if(trace) printf(\"TAB_EVENT(%d,page=%d)\\n\",i,val);\n',
                     '        if((ret=slotTabEvent(p,i,&d,val)) != 0) return ret;\n',
                     '        break;\n',
                     '      case TABLE_TEXT_EVENT:\n',
                     '        sscanf(text,\"(%d,%d,\",&x,&y);\n',
                     '        pvGetText(text,str1);\n',
                     '        if(trace) printf(\"TABLE_TEXT_EVENT(%d,%d,\\\"%s\\\")\\n\",x,y,str1);\n',
                     '        if((ret=slotTableTextEvent(p,i,&d,x,y,str1)) != 0) return ret;\n',
                     '        break;\n',
                     '      case TABLE_CLICKED_EVENT:\n',
                     '        sscanf(text,\"(%d,%d,%d)\",&x,&y,&button);\n',
                     '        if(trace) printf(\"TABLE_CLICKED_EVENT(%d,%d,button=%d)\\n\",x,y,button);\n',
                     '        if((ret=slotTableClickedEvent(p,i,&d,x,y,button)) != 0) return ret;\n',
                     '        break;\n',
                     '      case SELECTION_EVENT:\n',
                     '        sscanf(text,\"(%d,\",&val);\n',
                     '        pvGetText(text,str1);\n',
                     '        if(trace) printf(\"SELECTION_EVENT(column=%d,\\\"%s\\\")\\n\",val,str1);\n',
                     '        if((ret=slotSelectionEvent(p,i,&d,val,str1)) != 0) return ret;\n',
                     '        break;\n',
                     '      case CLIPBOARD_EVENT:\n',
                     '        sscanf(text,\"(%d\",&val);\n',
                     '        if(trace) printf(\"CLIPBOARD_EVENT(id=%d)\\n\",val);\n',
                     '        if(trace) printf(\"clipboard = \\n%s\\n\",p->clipboard);\n',
                     '        if((ret=slotClipboardEvent(p,i,&d,val)) != 0) return ret;\n',
                     '        break;\n',
                     '      case RIGHT_MOUSE_EVENT:\n',
                     '        if(trace) printf(\"RIGHT_MOUSE_EVENT id=%d text=%s\\n\",i,text);\n',
                     '        if((ret=slotRightMouseEvent(p,i,&d,text)) != 0) return ret;\n',
                     '        break;\n',
                     '      case KEYBOARD_EVENT:\n',
                     '        sscanf(text,\"(%d\",&val);\n',
                     '        if(trace) printf(\"KEYBOARD_EVENT modifier=%d key=%d\\n\",i,val);\n',
                     '        if((ret=slotKeyboardEvent(p,i,&d,val,i)) != 0) return ret;\n',
                     '        break;\n',
                     '      case PLOT_MOUSE_MOVED_EVENT:\n',
                     '        sscanf(text,\"(%f,%f)\",&xval,&yval);\n',
                     '        if(trace) printf(\"PLOT_MOUSE_MOVE %f %f\\n\",xval,yval);\n',
                     '        if((ret=slotMouseMovedEvent(p,i,&d,xval,yval)) != 0) return ret;\n',
                     '        break;\n',
                     '      case PLOT_MOUSE_PRESSED_EVENT:\n',
                     '        sscanf(text,\"(%f,%f)\",&xval,&yval);\n',
                     '        if(trace) printf(\"PLOT_MOUSE_PRESSED %f %f\\n\",xval,yval);\n',
                     '        if((ret=slotMousePressedEvent(p,i,&d,xval,yval)) != 0) return ret;\n',
                     '        break;\n',
                     '      case PLOT_MOUSE_RELEASED_EVENT:\n',
                     '        sscanf(text,\"(%f,%f)\",&xval,&yval);\n',
                     '        if(trace) printf(\"PLOT_MOUSE_RELEASED %f %f\\n\",xval,yval);\n',
                     '        if((ret=slotMouseReleasedEvent(p,i,&d,xval,yval)) != 0) return ret;\n',
                     '        break;\n',
                     '      case MOUSE_OVER_EVENT:\n',
                     '        sscanf(text,\"%d\",&val);\n',
                     '        if(trace) printf(\"MOUSE_OVER_EVENT %d\\n\",val);\n',
                     '        if((ret=slotMouseOverEvent(p,i,&d,val)) != 0) return ret;\n',
                     '        break;\n',
                     '      case USER_EVENT:\n',
                     '        if(trace) printf(\"USER_EVENT id=%d %s\\n\",i,text);\n',
                     '        if((ret=slotUserEvent(p,i,&d,text)) != 0) return ret;\n',
                     '        break;\n',
                     '      default:\n',
                     '        if(trace) printf(\"UNKNOWN_EVENT id=%d %s\\n\",i,text);\n',
                     '        break;\n',
                     '    }\n',
                     '  }\n',
                     ',"}\n'                  
] 
    with  open(mask_file,'w')  as mask_file_handler:
        mask_file_handler.writelines(lines_to_write) 

def generate_initial_slots(index):
    my_parameters = parameters.parameters()
    #TODO: different languages by plugins!
    if my_parameters.script == global_defines.PV_LUA:
        lua_generate_initial_slots(index)
    else: #C++
        cpp_generate_initial_slots(index)
                        
def lua_generate_initial_slots(index):
    print('LUA not implemented yet!')
    
def cpp_generate_initial_slots(index):
    slots_file = 'mask{0}_slots.h' 
    slots_file = slots_file.format(index)
    #slots_name = parse('{}_slots.h',slots_file)[0]
    #TODO: add license notice here!
    lines_to_write =['////////////////////////////////////////////////////////////////////////////\n',
                     '//\n',
                     '// {file_name} for ProcessViewServer created: {creation_date}\n'.format(file_name=slots_file,creation_date=datetime.datetime.now().strftime("%I:%M%p // %Y/%B/%d")),
                     '//\n',
                     '// please fill out these slots\n',
                     '// here you find all possible events\n',
                     '// Yours: pvbrowser\'s community\n',
                     '////////////////////////////////////////////////////////////////////////////\n',
                     '\n',
                     '// todo: uncomment me if you want to use this data aquisiton\n',
                     '// also uncomment this classes in main.cpp and pvapp.h\n',
                     '// also remember to uncomment rllib in the project file\n',
                     '//extern rlModbusClient     modbus;  //Change if applicable\n',
                     '//extern rlSiemensTCPClient siemensTCP;\n',
                     '//extern rlPPIClient        ppi;\n',
                     '\n',
                     'typedef struct // (todo: define your data structure here)\n',
                     '{\n',
                     '}\n',
                     'DATA;\n',
                     '\n',
                     'static int slotInit(PARAM *p, DATA *d)\n',
                     '{\n',
                     '  if(p == NULL || d == NULL) return -1;\n',
                     '  //memset(d,0,sizeof(DATA));\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotNullEvent(PARAM *p, DATA *d)\n',
                     '{\n',
                     '  if(p == NULL || d == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotButtonEvent(PARAM *p, int id, DATA *d)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotButtonPressedEvent(PARAM *p, int id, DATA *d)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotButtonReleasedEvent(PARAM *p, int id, DATA *d)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotTextEvent(PARAM *p, int id, DATA *d, const char *text)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || text == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotSliderEvent(PARAM *p, int id, DATA *d, int val)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || val < -1000) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotCheckboxEvent(PARAM *p, int id, DATA *d, const char *text)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || text == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotRadioButtonEvent(PARAM *p, int id, DATA *d, const char *text)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || text == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotGlInitializeEvent(PARAM *p, int id, DATA *d)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotGlPaintEvent(PARAM *p, int id, DATA *d)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotGlResizeEvent(PARAM *p, int id, DATA *d, int width, int height)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || width < 0 || height < 0) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotGlIdleEvent(PARAM *p, int id, DATA *d)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotTabEvent(PARAM *p, int id, DATA *d, int val)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || val < -1000) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotTableTextEvent(PARAM *p, int id, DATA *d, int x, int y, const char *text)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || x < -1000 || y < -1000 || text == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotTableClickedEvent(PARAM *p, int id, DATA *d, int x, int y, int button)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || x < -1000 || y < -1000 || button < 0) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotSelectionEvent(PARAM *p, int id, DATA *d, int val, const char *text)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || val < -1000 || text == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotClipboardEvent(PARAM *p, int id, DATA *d, int val)\n',
                     '{\n',
                     '  if(p == NULL || id == -1 || d == NULL || val < -1000) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotRightMouseEvent(PARAM *p, int id, DATA *d, const char *text)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || text == NULL) return -1;\n',
                     '  //pvPopupMenu(p,-1,\"Menu1,Menu2,,Menu3\");\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotKeyboardEvent(PARAM *p, int id, DATA *d, int val, int modifier)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || val < -1000 || modifier < -1000) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotMouseMovedEvent(PARAM *p, int id, DATA *d, float x, float y)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || x < -1000 || y < -1000) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotMousePressedEvent(PARAM *p, int id, DATA *d, float x, float y)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || x < -1000 || y < -1000) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotMouseReleasedEvent(PARAM *p, int id, DATA *d, float x, float y)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || x < -1000 || y < -1000) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotMouseOverEvent(PARAM *p, int id, DATA *d, int enter)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || enter < -1000) return -1;\n',
                     '  return 0;\n',
                     '}\n',
                     '\n',
                     'static int slotUserEvent(PARAM *p, int id, DATA *d, const char *text)\n',
                     '{\n',
                     '  if(p == NULL || id == 0 || d == NULL || text == NULL) return -1;\n',
                     '  return 0;\n',
                     '}\n'
] 
    with  open(slots_file,'w')  as slots_file_handler:
        slots_file_handler.writelines(lines_to_write)         
        
def add_mask_to_project(qmake_project_file, index):
    my_parameters = parameters.parameters()
    
    if(my_parameters.arg_debug):
        print('add_mask_to_project mask_index=%d qmake_pro_file_name=%s\n'% (index,qmake_project_file))
        
    file_handler = open(qmake_project_file, 'r+')
    file_content = file_handler.readlines()
    new_file_content = []
    for line in file_content:
        new_file_content.append(line)
        if re.search('HEADERS',line) and re.search('pvapp.h',line):
            new_file_content.append('           mask{0}_slots.h \\\n'.format(index))
        elif re.search('SOURCES',line) and re.search('main.cpp',line):
            new_file_content.append('           mask{0}.cpp \\\n'.format(index))

    file_handler.seek(0)
    file_handler.writelines(new_file_content)   
    file_handler.close()
    
def add_mask_to_main(index):
    my_parameters = parameters.parameters()
    #TODO: different languages by plugins!
    if my_parameters.script == global_defines.PV_LUA:
        lua_add_mask_to_main(index)
    else: #C++
        cpp_add_mask_to_main(index)
        
def lua_add_mask_to_main(index):
    print('LUA not implemented yet!')

def cpp_add_mask_to_main(index):
    my_parameters = parameters.parameters()   
    
    if(my_parameters.arg_debug):
        print('cpp_add_mask_to_main mask_index=%d'% (index))
        
    file_handler = open('main.cpp', 'r+')
    file_content = file_handler.readlines()
    new_file_content = []
    while_found = False
    switch_found = False
    case_found = False
    done = False
    
    for line in file_content:
        if (not while_found) and re.search('while\(1\)',line):
            while_found = True            
            print('while found!')
        if while_found and (not switch_found) and re.search('switch\(ret\)',line):
            switch_found = True
            print('switch found!')
        if while_found and switch_found and (not case_found) and re.search('case',line):
            print('case found!')
            case_found = True        
        if while_found and switch_found and case_found and (not done) and re.search('case',line):
            new_file_content.append('      case {0}:\n'.format(index))
            new_file_content.append('        pvStatusMessage(p,-1,-1,-1,\"mask{0}\');\n'.format(index))
            new_file_content.append('        ret = show_mask{0}(p);\n'.format(index))
            new_file_content.append('        break;\n')
            new_file_content.append(line)
            done = True
        elif while_found and switch_found and (not done) and re.search('default',line):
            new_file_content.append('      case {0}:\n'.format(index))
            new_file_content.append('        pvStatusMessage(p,-1,-1,-1,\"mask{0}\');\n'.format(index))
            new_file_content.append('        ret = show_mask{0}(p);\n'.format(index))
            new_file_content.append('        break;\n')
            new_file_content.append(line)           
        else:
            new_file_content.append(line)
            
    file_handler.seek(0)
    file_handler.writelines(new_file_content)   
    file_handler.close()
    
def add_mask_to_header(index):
    my_parameters = parameters.parameters()
    if(my_parameters.arg_debug):
        print('add_mask_to_header mask_index=%d'% (index))
        
    file_handler = open('pvapp.h', 'r+')
    file_content = file_handler.readlines()
    new_file_content = []
    done = False
    for line in file_content:
        if (not done) and line[:3] == 'int' and re.search('int show_mask',line):
            new_file_content.append('int show_mask{0}(PARAM *p);\n'.format(index))
            new_file_content.append(line)           
            done = True
        else:
            new_file_content.append(line)
  

    file_handler.seek(0)
    file_handler.writelines(new_file_content)   
    file_handler.close()