import tkinter.tix as tix

def print_selected(args):
    print('selected dir:', args)

root = tix.Tk()
dialog = tix.DirSelectDialog(root, command=print_selected)
dialog.popup()
