import tkinter as tk
from tkinter import ttk, messagebox
from typing import Literal
from datetime import date, datetime

from tab import Tab
from top_level import TopLevel
import config
from database import db
from grid import Grid

class Window:
    grids: list[Grid]
    grids = {}
    def __init__(self, title, width=900, height=600):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(f'{width}x{height}+{self.window.winfo_screenwidth() // 2 - width // 2}+{self.window.winfo_screenheight() // 2 - height // 2}')

        self.button_frame = None
        self.notebook = None

    def start(self):
        self.window.mainloop()

    def new_button(self, text, command):
        if self.button_frame is None:
            self.button_frame = tk.Frame(self.window)
            self.button_frame.pack(fill='y', side='left', padx=10)

        button = tk.Button(self.button_frame, text=text, command=command)
        return button

    def new_tab(self, text):
        if self.notebook is None:
            self.notebook = ttk.Notebook(self.window)
            self.notebook.pack(expand=True, fill='both')

        tab = Tab(self.notebook, text)
        return tab

    def row(self, action: Literal['add', 'change', 'delete']):
        table = self.notebook.tab('current', 'text')
        if action == 'delete':
            id:tuple
            id = Window.grids[table].get_selected_rows()
            if len(id) == 0:
                messagebox.showinfo('Предупреждение', 'Не выбраны записи для удаления', icon='warning')
                return
            try:
                db.delete(table, id)
            except:
                messagebox.showinfo('Ошибка', 'Нельзя удалить запись: она используется в других таблицах!', icon='error')
                return
            Window.grids[table].update()
        elif action == 'add' or action == 'change':
            if action == 'change':
                id = Window.grids[table].get_selected_rows()
                if len(id) != 1:
                    messagebox.showinfo('Предупреждение', 'Не выбрана запись для изменения' if len(id) == 0 else 'Выберите одну запись', icon='warning')
                    return
                _, rows = db.select(f'SELECT * FROM {table} WHERE ID = {id[0]}')
            fields = Window.grids[table].FIELDS
            new_fields = []
            for i in range(1, len(fields)):
                n, t = fields[i]
                if n in config.TABLES:
                    t = Grid
                new_fields.append((n, t))
            TopLevel(
                self.window,
                f'Добавить {table}' if action == 'add' else f'Изменить {table}',
                new_fields,
                rows[0][1:] if action == 'change' else None,
                callback=lambda fields, values: self.__insert_callback(table, fields, values) if action == 'add' else self.__update_callback(table, fields, values, int(id[0]))
            )

    def __insert_callback(self, table, fields, values):
        id = db.insert(table, fields, values)
        grid = Window.grids[table]
        grid.update()
        grid.select_row_by_id(id)

    def __update_callback(self, table, fields, values, id):
        db.update(table, fields, values, id)
        grid = Window.grids[table]
        grid.update()
        grid.select_row_by_id(id)

def __main__():
    window = Window('Театр')
    window.new_button('Добавить', lambda: window.row('add')).pack(pady=10)
    window.new_button('Изменить', lambda: window.row('change')).pack(pady=10)
    window.new_button('Удалить', lambda: window.row('delete')).pack(pady=10)
    
    for title, info in config.TABLES.items():
        if title == 'Режиссёр':
            continue
        tab = window.new_tab(title)
        Window.grids[title] = tab.new_grid(info['query'])
    window.start()

if __name__ == '__main__':
    __main__()