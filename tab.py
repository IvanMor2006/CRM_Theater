import tkinter as tk
from tkinter import ttk

from grid import Grid

class Tab:
    def __init__(self, notebook, text):
        self.title = text
        self.element = ttk.Frame(notebook)
        notebook.add(self.element, text=text)
    
    def new_grid(self, query):
        self.grid = Grid(self.element, query)
        return self.grid