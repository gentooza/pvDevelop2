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
from tkinter.messagebox import showinfo


class helpMenu():
    def about(root):
        my_msg = ("This a basic text editor implemented"
                  "in Python's Tkinter")
        showinfo(title="About",
                 message=my_msg)

    def __init__(self, text, root, mainWin):
        helpMenu = tk.Menu(mainWin.menubar, tearoff=0)
        helpMenu.add_command(label="About", command=self.about)
        mainWin.menubar.add_cascade(label="Help", menu=helpMenu)

        root.config(menu=mainWin.menubar)
