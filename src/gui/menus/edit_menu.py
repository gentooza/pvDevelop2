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
import tkinter.simpledialog as tksimpledialog
# from tkinter.filedialog import *
# from tkinter.messagebox import *


class editMenu():

    def build_edit_menu(self):
        self.editMenu.add_command(label="Copy",
                                  command=self.copy,
                                  accelerator="Ctrl+C")
        self.editMenu.add_command(label="Cut",
                                  command=self.cut,
                                  accelerator="Ctrl+X")
        self.editMenu.add_command(label="Paste",
                                  command=self.paste,
                                  accelerator="Ctrl+V")
        self.editMenu.add_command(label="Undo",
                                  command=self.undo,
                                  accelerator="Ctrl+Z")
        self.editMenu.add_command(label="Redo",
                                  command=self.redo,
                                  accelerator="Ctrl+Y")
        self.editMenu.add_command(label="Find",
                                  command=self.find,
                                  accelerator="Ctrl+F")
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Select All",
                                  command=self.select_all,
                                  accelerator="Ctrl+A")
        self.mainWin.menubar.add_cascade(label="Edit", menu=self.editMenu)

    def popup(self, event):
        self.rightClick.post(event.x_root, event.y_root)

    def copy(self, *args):
        sel = self.text.selection_get()
        self.clipboard = sel

    def cut(self, *args):
        sel = self.text.selection_get()
        self.clipboard = sel
        self.text.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def paste(self, *args):
        self.text.insert(tk.INSERT, self.clipboard)

    def select_all(self, *args):
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(0.0, tk.END)
        self.text.see(tk.INSERT)

    def undo(self, *args):
        self.text.edit_undo()

    def redo(self, *args):
        self.text.edit_redo()

    def find(self, *args):
        self.text.tag_remove('found', '1.0', tk.END)
        target = tksimpledialog.askstring('Find', 'Search String:')
        if target:
            idx = '1.0'
            while 1:
                idx = self.text.search(target, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                lastidx = '%s+%dc' % (idx, len(target))
                self.text.tag_add('found', idx, lastidx)
                idx = lastidx
            self.text.tag_config('found',
                                 foreground='white',
                                 background='blue')

    def update(self):
        if ((not self.mainWin.selectedText)
                or (self.mainWin.selectedText == '')):
            self.editMenu.entryconfig("Copy", state="disabled")
            self.editMenu.entryconfig("Cut", state="disabled")
            self.rightClick.entryconfig(1, state="disabled")
            self.rightClick.entryconfig(2, state="disabled")
        else:
            self.editMenu.entryconfig("Copy", state="normal")
            self.editMenu.entryconfig("Cut", state="normal")
            self.rightClick.entryconfig(1, state="normal")
            self.rightClick.entryconfig(2, state="normal")

    def __init__(self, text, root, mainWin):
        self.clipboard = None
        self.text = text
        self.mainWin = mainWin
        self.rightClick = tk.Menu(root)
        self.editMenu = tk.Menu(mainWin.menubar, tearoff=0)
        self.build_edit_menu()

        root.bind_all("<Control-z>", self.undo)
        root.bind_all("<Control-y>", self.redo)
        root.bind_all("<Control-f>", self.find)
        root.bind_all("Control-a", self.select_all)

        self.rightClick.add_command(label="Copy", command=self.copy)
        self.rightClick.add_command(label="Cut", command=self.cut)
        self.rightClick.add_command(label="Paste", command=self.paste)
        self.rightClick.add_separator()
        self.rightClick.add_command(label="Select All",
                                    command=self.select_all)
        self.rightClick.bind("<Control-q>", self.select_all)

        self.text.bind("<Button-3>", self.popup)

        root.config(menu=mainWin.menubar)

        self.update()
