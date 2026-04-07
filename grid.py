import tkinter as tk
from tkinter import ttk

from database import db

class Grid:
    def __init__(self, parent, query, select_many_raws=True):
        self.QUERY = query
        self.FIELDS, self.rows = db.select(self.QUERY)

        COLUMNS = ['#' + str(i + 1) for i in range(len(self.FIELDS))]
        widths = self.calc_widths()
        
        self.frame = tk.Frame(parent)
        self.frame.pack(fill='y', side='left')
        self.frame.config(takefocus=False)

        self.button = tk.Button(self.frame, text='Снять выделение', command=lambda: self.element.selection_set([]))
        self.button.pack(side='bottom')

        scrollbar_x = ttk.Scrollbar(self.frame, orient='horizontal')
        scrollbar_x.pack(side='bottom', fill='x')
        scrollbar_y = ttk.Scrollbar(self.frame)
        scrollbar_y.pack(side='right', fill='y')

        self.element = ttk.Treeview(self.frame, columns=COLUMNS, show='headings', selectmode='extended' if select_many_raws else 'browse', xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        self.element.config(takefocus=False)
        scrollbar_x.config(command=self.element.xview)
        scrollbar_y.config(command=self.element.yview)

        for row in self.rows:
            self.element.insert('', 'end', values=tuple(row))
        for f, c, w in zip(self.FIELDS, COLUMNS, widths):
            n, t = f
            if 'ID' in n:
                w = 0
            self.element.heading(c, text=n)
            self.element.column(c, width=w, stretch=False)
        self.element.pack(expand=True, fill='both')

    def select_row_by_id(self, id):
        for item in self.element.get_children():
            buf_id = int(self.element.item(item, 'values')[0])
            if buf_id == id:
                self.element.selection_set(item)
                self.element.see(item)
                return True
        return False
        
    def get_selected_rows(self):
        id = []
        rows_id = self.element.selection()
        for row_id in rows_id:
            id.append(self.element.item(row_id, 'values')[0])
        return id

    def update(self):
        self.clear()
        _, self.rows = db.select(self.QUERY)
        for row in self.rows:
            self.element.insert('', 'end', values=tuple(row))

    def clear(self):
        self.element.delete(*self.element.get_children())

    def calc_widths(self):
        char_size = 9
        widths = []
        for i in range(len(self.FIELDS)):
            max_len = len(self.FIELDS[i][0])
            for row in self.rows:
                max_len = max(len(str(row[i])), max_len)
            widths.append(max_len * char_size)
        return widths
