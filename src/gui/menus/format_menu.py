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
from tkinter.colorchooser import askcolor
from tkinter.font import Font, families
# from ScrolledText import *
import time


class formatMenu():

    def change_bg(self):
        (triple, hexstr) = askcolor()
        if hexstr:
            self.text.config(bg=hexstr)

    def change_fg(self):
        (triple, hexstr) = askcolor()
        if hexstr:
            self.text.config(fg=hexstr)

    def bold(self, *args):	 # Works only if text is selected
        try:
            current_tags = self.text.tag_names("sel.first")
            if "bold" in current_tags:
                self.text.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text.tag_add("bold", "sel.first", "sel.last")
                bold_font = Font(self.text, self.text.cget("font"))
                bold_font.configure(weight="bold")
                self.text.tag_configure("bold", font=bold_font)
        except:
            pass

    def italic(self, *args):  # Works only if text is selected
        try:
            current_tags = self.text.tag_names("sel.first")
            if "italic" in current_tags:
                self.text.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text.tag_add("italic", "sel.first", "sel.last")
                italic_font = Font(self.text, self.text.cget("font"))
                italic_font.configure(slant="italic")
                self.text.tag_configure("italic", font=italic_font)
        except:
            pass

    def underline(self, *args):	 # Works only if text is selected
        try:
            current_tags = self.text.tag_names("sel.first")
            if "underline" in current_tags:
                self.text.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.text.tag_add("underline", "sel.first", "sel.last")
                underline_font = Font(self.text, self.text.cget("font"))
                underline_font.configure(underline=1)
                self.text.tag_configure("underline", font=underline_font)
        except:
            pass

    def overstrike(self, *args):  # Works only if text is selected
        try:
            current_tags = self.text.tag_names("sel.first")
            if "overstrike" in current_tags:
                self.text.tag_remove("overstrike", "sel.first", "sel.last")
            else:
                self.text.tag_add("overstrike", "sel.first", "sel.last")
                overstrike_font = Font(self.text, self.text.cget("font"))
                overstrike_font.configure(overstrike=1)
                self.text.tag_configure("overstrike", font=overstrike_font)
        except:
            pass

    def addDate(self):
        full_date = time.localtime()
        day = str(full_date.tm_mday)
        month = str(full_date.tm_mon)
        year = str(full_date.tm_year)
        date = day + '/' + month + '/' + year
        self.text.insert(tk.INSERT, date, "a")

    def __init__(self, text, root, mainWin):
        self.text = text
        self.root = root
        self.mainWin = mainWin

        fontoptions = families(root)
        font = Font(family="Verdana", size=10)
        formatMenu = tk.Menu(mainWin.menubar, tearoff=0)
        fsubmenu = tk.Menu(formatMenu, tearoff=0)
        ssubmenu = tk.Menu(formatMenu, tearoff=0)

        for option in fontoptions:
            fsubmenu.add_command(label=option,
                                 command=lambda:
                                     font.configure(family=option))
        for value in range(1, 31):
            ssubmenu.add_command(label=str(value),
                                 command=lambda:
                                     font.configure(size=value))

        formatMenu.add_command(label="Change Background",
                               command=self.change_bg)
        formatMenu.add_command(label="Change Font Color",
                               command=self.change_fg)
        formatMenu.add_cascade(label="Font",
                               underline=0, menu=fsubmenu)
        formatMenu.add_cascade(label="Size",
                               underline=0, menu=ssubmenu)
        formatMenu.add_command(label="Bold",
                               command=self.bold,
                               accelerator="Ctrl+B")
        formatMenu.add_command(label="Italic",
                               command=self.italic,
                               accelerator="Ctrl+I")
        formatMenu.add_command(label="Underline",
                               command=self.underline,
                               accelerator="Ctrl+U")
        formatMenu.add_command(label="Overstrike",
                               command=self.overstrike,
                               accelerator="Ctrl+T")
        formatMenu.add_command(label="Add Date",
                               command=self.addDate)
        mainWin.menubar.add_cascade(label="Format",
                                    menu=formatMenu)

        root.bind_all("<Control-b>", self.bold)
        root.bind_all("<Control-i>", self.italic)
        root.bind_all("<Control-u>", self.underline)
        root.bind_all("<Control-T>", self.overstrike)

        root.grid_columnconfigure(0, weight=1)
        root.resizable(True, True)

        root.config(menu=mainWin.menubar)
