#!/usr/bin/env python3

"""
This file is part of pyPvDevelop.

Copyright 2023, Joaquín Cuéllar-

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
import sys
try:
    import tkinter as tk
    from tkinter.font import Font
    from tkinter import scrolledtext
    from src import paths
    import parameters
    import global_defines
    from parse import parse
    import file_menu
    import edit_menu
    import format_menu
    import help_menu
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)

class MainWindow():

    def __init__(self, master = None):
        self.master = master
        my_parameters = parameters.parameters()
        if my_parameters.arg_project:
            my_title = my_parameters.arg_project + ' - Python Pvbrowser Developer'
        else:
            my_title = 'No project loaded - Python Pvbrowser Developer'
        self.master.title(my_title)
        self.font = Font(family="Verdana", size=10)
        self.text = scrolledtext.ScrolledText(self.master, state='normal',
                                 height=400, width=400,
                                 wrap='word',
                                 font=self.font, pady=2,
                                 padx=3, undo=True, bg='white')
        self.text.pack(fill=tk.Y, expand=1)
        self.text.focus_set()
        self.menubar = tk.Menu(self.master, relief=tk.FLAT)
        self.selectedText = None
        '''configure events'''
        self.events()

    def build(self):
        self.fileMenu = file_menu.fileMenu(self.text, self.master, self)
        self.editMenu = edit_menu.editMenu(self.text, self.master, self)
        self.formatMenu = format_menu.formatMenu(self.text, self.master, self)
        self.helpMenu = help_menu.helpMenu(self.text, self.master, self)
    
    def events(self):
        self.text.bind("<<Selection>>", self.evSelectedText)
        self.master.bind("<Button-1>", self.evMouseClick)
        self.menubar.bind("<Button-1>", self.evMouseClick)

    '''EVENTS'''
    def evSelectedText(self, event):
        oldSelectedText = self.selectedText
        try:
            self.selectedText = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except:
            self.selectedText = None
        ''' update edit menu'''
        if oldSelectedText != self.selectedText:
            self.editMenu.update()

    def evMouseClick(self, event):
        self.editMenu.rightClick.unpost()
