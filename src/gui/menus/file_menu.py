#!/usr/bin/env python3
'''
Copyright (C) 2015 Punith Patil
Copyright (C) 2019-2020 Joaquín Cuéllar

This file is part of Basic Simple Text Editor.

Basic Simple Text Editor is free software:
you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Basic Simple Text Editor is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Basic Simple Text Editor.
If not, see <https://www.gnu.org/licenses/>.
'''

import tkinter as tk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox


class fileMenu():

    def build_menu(self):
        self.fileMenu.add_command(label="New",
                                  command=self.new_file)
        self.fileMenu.add_command(label="Open",
                                  command=self.open_file)
        self.fileMenu.add_command(label="Save",
                                  command=self.save_file)
        self.fileMenu.add_command(label="Save As...",
                                  command=self.save_as)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Quit",
                                  command=self.quit)
        self.mainWin.menubar.add_cascade(label="File",
                                         menu=self.fileMenu)
        self.root.config(menu=self.mainWin.menubar)

    def new_file(self):
        self.filename = "Untitled"
        self.text.delete(0.0, tk.END)

    def save_file(self):
        try:
            t = self.text.get(0.0, tk.END)
            f = open(self.filename, 'w')
            f.write(t)
            f.close()
        except:
            self.saveAs()

    def save_as(self):
        f = tkfiledialog.asksaveasfile(mode='w', defaultextension='.txt')
        t = self.text.get(0.0, tk.END)
        try:
            f.write(t.rstrip())
        except:
            tkmessagebox.showerror(title="Oops!",
                                   message="Unable to save file...")

    def open_file(self):
        f = tkfiledialog.askopenfile(mode='r')
        self.filename = f.name
        t = f.read()
        self.text.delete(0.0, tk.END)
        self.text.insert(0.0, t)
        self.main_win.set_app_title(f.name)

    def quit(self):
        entry = tkmessagebox.askyesno(title="Quit",
                                      message="Are you sure you want to quit?")
        if entry is True:
            self.root.destroy()

    def __init__(self, text, root, mainWin):
        self.fileName = None
        self.text = text
        self.root = root
        self.mainWin = mainWin

        self.fileMenu = tk.Menu(mainWin.menubar, tearoff=0)
        self.build_menu()
