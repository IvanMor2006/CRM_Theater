import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime
from decimal import Decimal

import config
from grid import Grid
from child_window import ChildWindow

class IUForm:
    def __init__(self, parent, title, fields, current_values, callback=None):
        size = config.TABLES[title.split()[1]]['size']
        self.window = ChildWindow(parent, title, size)

        self.callback = callback
        self.elements = {}

        if current_values is None:
            current_values = [''] * len(fields)

        focused = False
        for (n, t), value in zip(fields, current_values):
            frame = tk.Frame(self.window.element)
            frame.pack(fill='x', padx=50, pady=5)
            label = tk.Label(frame, text=n)
            if t == Grid:
                label.pack()
                element = Grid(frame, config.TABLES[n]['query'], False)
                element.frame.pack(expand=True, fill='x')
                if value:
                    element.select_row_by_id(value)
            else:
                element = tk.Entry(frame)
                element.pack(expand=True, fill='x', side='right')
                label.pack(side='right')
                if value:
                    element.insert(0, value)
                elif n in config.DEFUALT_FIELDS:
                    raw_data = config.DEFUALT_FIELDS[n]
                    element.insert(0, raw_data() if callable(raw_data) else raw_data)
                if not focused:
                    focused = True
                    element.focus()
                element.bind('<Return>', lambda event: self.get_data())
            self.elements[n] = element, t

        button = tk.Button(self.window.element, text=title, command=self.get_data)
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
                            data = 'NULL'
                        elif n in config.DEFUALT_FIELDS:
                            row_data = config.DEFUALT_FIELDS[n]
                            data = row_data() if callable(row_data) else row_data
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
                    messagebox.showerror('Ошибка', f'Неверный тип данных в поле {n}', parent=self.window.element)
                    element.focus()
                elif isinstance(element, Grid):
                    messagebox.showerror('Ошибка', f'Выберите строку в таблице {n}', parent=self.window.element)
                return None
            result[n] = data
        print(result)
        try:
            if self.callback:
                self.callback(list(result.keys()), tuple(result.values()))
            self.window.element.destroy()
        except Exception as e:
            print(e)
            for error, message in config.CONSTRAINTS.items():
                if error in str(e):
                    messagebox.showwarning('Предупреждение', message)
                    break