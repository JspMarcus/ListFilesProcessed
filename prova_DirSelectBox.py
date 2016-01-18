#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.tix as tix

root = tix.Tk()

def print_selected(args):
    print('selected dir:', args)

def pathSelect():
    d = tix.DirSelectBox(master=root, command=print_selected)
    

button = Button(root, text="dialog", command=pathSelect)
button.pack()

root.mainloop()
