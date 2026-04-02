import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime
from decimal import Decimal

import config
from grid import Grid

class TopLevel:
    def __init__(self, parent, title, fields, current_values, callback=None):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        size = config.TABLES[title.split()[1]]['size']
        width, height = size.split('x')
        self.window.geometry(size)
        self.window.geometry(f'+{self.window.winfo_screenwidth() // 2 - int(width) // 2}+{self.window.winfo_screenheight() // 2 - int(height) // 2}')
        
        self.window.transient(parent)
        self.window.grab_set()

        self.callback = callback
        self.elements = {}

        if current_values is None:
            current_values = [''] * len(fields)

        focused = False
        for (n, t), value in zip(fields, current_values):
            frame = tk.Frame(self.window)
            frame.pack(fill='x', padx=50, pady=5)
            label = tk.Label(frame, text=n)
            if t == Grid:
                label.pack()
                element = Grid(frame, config.TABLES[n]['query'], False)
                element.frame.pack(expand=True, fill='x')
                if value:
                    for item in element.element.get_children():
                        buf_id = int(element.element.item(item, 'values')[0])
                        if buf_id == value:
                            break
                    element.element.selection_set(item)
            else:
                element = tk.Entry(frame)
                element.pack(expand=True, fill='x', side='right')
                label.pack(side='right')
                element.insert(0, value)
                if not focused:
                    focused = True
                    element.focus()
            self.elements[n] = element, t

        button = tk.Button(self.window, text=title, command=self.get_data)
        button.pack()

    def get_data(self):
        result = {}
        for n, entryAndType in self.elements.items():
            element, t = entryAndType
            try:
                if isinstance(element, tk.Entry):
                    element: tk.Entry
                    if not (data_str := element.get()):
                        if n in config.NULL_FIELDS:
                            if n == 'Цена':
                                data = config.DEFAULT_PRICE
                            else:
                                data = 'NULL'
                        else:
                            raise
                    else:
                        if t == date:
                            datetime.strptime(data_str, '%Y-%m-%d').date()
                            data = data_str
                        elif t == datetime:
                            try:
                                datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
                                data = data_str
                            except:
                                data_obj = datetime.strptime(data_str, '%Y-%m-%d %H:%M')
                                data = data_obj.strftime('%Y-%m-%d %H:%M:%S')
                        elif t == Decimal:
                            data = float(data_str)
                        else:
                            data = t(data_str)
                elif (element, Grid):
                    element: Grid
                    id = element.get_selected_rows()
                    if len(id) == 0:
                        if config.TABLES[n]['IDTable'] in config.NULL_FIELDS:
                            data = 'NULL'
                        else:
                            raise
                    else:
                        data = int(id[0])
                    n = config.TABLES[n]['IDTable']
            except:
                if isinstance(element, tk.Entry):
                    messagebox.showinfo('Ошибка', f'Неверный тип данных в поле {n}', icon='error', parent=self.window)
                    element.focus()
                elif isinstance(element, Grid):
                    messagebox.showinfo('Ошибка', f'Выберите строку в таблице {n}', icon='error', parent=self.window)
                return None
            result[n] = data
        print(result)
        try:
            if self.callback:
                self.callback(list(result.keys()), tuple(result.values()))
            self.window.destroy()
        except Exception as e:
            print(e)
            for error, message in config.CONSTRAINTS.items():
                if error in str(e):
                    messagebox.showinfo('Предупреждение', message, icon='warning')
                    break