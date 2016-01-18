#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.tix as tix

root = tix.Tk()

def print_selected(args):
    print('selected dir:', args)

def pathSelect():
    d = tix.DirSelectDialog(master=root, command=print_selected)
    d.popup()

button = Button(root, text="dialog", command=pathSelect)
button.pack()

root.mainloop()
