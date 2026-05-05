import tkinter as tk

class ChildWindow:
    def __init__(self, parent, title, size='1200x600'):
        self.element = tk.Toplevel(parent)
        self.element.title(title)
        self.element.geometry(size)
        width, height = size.split('x')
        self.element.geometry(f'+{self.element.winfo_screenwidth() // 2 - int(width) // 2}+{self.element.winfo_screenheight() // 2 - int(height) // 2}')
        self.element.transient(parent)
        self.element.grab_set()