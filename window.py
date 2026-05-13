import tkinter as tk
from tkinter import ttk, messagebox
from typing import Literal

import config
from tab import Tab
from iuform import IUForm
from menu import Menu
from database import db
from grid import Grid
from child_window import ChildWindow

class Window:
    def __init__(self, title, width=900, height=600):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(f'{width}x{height}+{self.window.winfo_screenwidth() // 2 - width // 2}+{self.window.winfo_screenheight() // 2 - height // 2}')

        self.window.bind('<Escape>', lambda event: self.window.destroy())

        self.button_frame = None
        self.notebook = None

        self.menu = Menu(self)

        self.grids: dict[str, Grid] = {}
        self.buttons: dict[str, tk.Button] = {}

    def check_rows(self, *args):
        _, grid = self.get_current_grid()
        if not grid.rows:
            self.buttons['Изменить'].config(state=tk.DISABLED)
            self.buttons['Удалить'].config(state=tk.DISABLED)
        else:
            self.buttons['Изменить'].config(state=tk.NORMAL)
            self.buttons['Удалить'].config(state=tk.NORMAL)

    def start(self):
        self.window.mainloop()

    def new_button(self, text, command):
        if self.button_frame is None:
            self.button_frame = tk.Frame(self.window)
            self.button_frame.pack(fill='y', side='left', padx=10)
        button = tk.Button(self.button_frame, text=text, command=command)
        self.buttons[text] = button
        return button

    def new_tab(self, text):
        if self.notebook is None:
            self.notebook = ttk.Notebook(self.window)
            self.notebook.pack(expand=True, fill='both')
            self.notebook.bind("<<NotebookTabChanged>>", self.check_rows)
        tab = Tab(self.notebook, text)
        return tab

    def get_current_grid(self) -> tuple[str, Grid]:
        table = self.notebook.tab('current', 'text')
        return table, self.grids[table]

    def row(self, action: Literal['add', 'change', 'delete']):
        table, grid = self.get_current_grid()
        if action == 'delete':
            id:tuple
            id = grid.get_selected_rows()
            if len(id) == 0:
                messagebox.showwarning('Предупреждение', 'Не выбраны записи для удаления')
                return
            try:
                db.delete(table, id)
            except Exception as e:
                messagebox.showerror('Ошибка', 'Нельзя удалить запись: она используется в других таблицах!')
                return
            grid.update()
            self.check_rows()
        elif action == 'add' or action == 'change':
            if action == 'change':
                id = grid.get_selected_rows()
                if len(id) != 1:
                    messagebox.showwarning('Предупреждение', 'Не выбрана запись для изменения' if len(id) == 0 else 'Выберите одну запись')
                    return
                _, rows = db.select(f'SELECT * FROM {table} WHERE ID = {id[0]}')
            fields = grid.FIELDS
            new_fields = []
            for i in range(1, len(fields)):
                n, t = fields[i]
                if n in config.TABLES:
                    t = Grid
                new_fields.append((n, t))
            IUForm(
                self.window,
                f'Добавить {table}' if action == 'add' else f'Изменить {table}',
                new_fields,
                rows[0][1:] if action == 'change' else None,
                callback=lambda fields, values: self.__insert_callback(table, fields, values) if action == 'add' else self.__update_callback(table, fields, values, int(id[0]))
            )

    def __insert_callback(self, table, fields, values):
        id = db.insert(table, fields, values)
        grid = self.grids[table]
        grid.update()
        self.check_rows()
        grid.select_row_by_id(id)

    def __update_callback(self, table, fields, values, id):
        db.update(table, fields, values, id)
        grid = self.grids[table]
        grid.update()
        self.check_rows()
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
        window.grids[title] = tab.new_grid(info['query'])
        if title == 'Билет':
            def log():
                query = '''
                    SELECT *
                    FROM БилетыLog
                    ORDER BY datelog DESC, ID DESC
                '''
                log_window = ChildWindow(window.window, 'Log Билетов')
                log_window.element.focus()
                check_frame = tk.Frame(log_window.element)
                check_frame.del_val = tk.BooleanVar()
                def filt():
                    conditions = []
                    if check_frame.del_val.get():
                        conditions.append("typelog = 'D'")
                    if check_frame.ins_val.get():
                        conditions.append("typelog = 'I'")
                    where = f'WHERE {" OR ".join(conditions)}' if conditions else ''
                    log_window.grid.QUERY = f'''
                    SELECT *
                    FROM БилетыLog
                    {where}
                    ORDER BY datelog DESC, ID DESC
                    '''
                    if conditions:
                        log_window.grid.update()
                    else:
                        log_window.grid.clear()
                deleted_cb = tk.Checkbutton(check_frame, text='Удалённые', variable=check_frame.del_val, command=filt)
                deleted_cb.pack(side='left', expand=True)
                check_frame.del_val.set(True)
                check_frame.ins_val = tk.BooleanVar()
                inserted_cb = tk.Checkbutton(check_frame, text='Добавленные', variable=check_frame.ins_val, command=filt)
                inserted_cb.pack(side='left', expand=True)
                check_frame.ins_val.set(True)
                check_frame.pack()
                log_window.grid = Grid(log_window.element, query, False)
                log_window.grid.frame.pack(padx=10, pady=10, side='top', fill='both', expand=True)
                def restore():
                    try:
                        id = log_window.grid.get_selected_rows()[0]
                        if not db.query(f'''DECLARE @date DATETIME = (SELECT datelog FROM БилетLog WHERE ID = {id})
                                            EXEC ВосстановлениеБилетовДо {id}, @date'''):
                            messagebox.showerror('Ошибка', 'Невозможно восстановить билет на несуществующее представление!', parent=log_window.element)
                        log_window.grid.update()
                        window.grids['Билет'].update()
                    except:
                        messagebox.showwarning('Предупреждение', 'Выберите до какой записи восстановить билеты!', parent=log_window.element)
                tk.Button(log_window.grid.button_frame, text='Восстановить', command=restore).pack(side='left', expand=True, anchor='w', padx=20)
                log_window.grid.button.pack(anchor='e')
            tk.Button(window.grids[title].button_frame, text='Log', command=log).pack(side='left', expand=True, anchor='w', padx=20)
            window.grids[title].button.pack(anchor='e')
        if title == 'Представление':
            def delete_performances():
                grid: Grid = window.grids['Представление']
                rows = grid.get_selected_rows()
                if not rows:
                    messagebox.showwarning('Предупреждение', 'Выберите нужные представления!')
                    return
                for id in rows:
                    db.query(f'EXEC ОтменаПредставления {id}')
                    window.grids['Билет'].update()
                    grid.update()
                window.check_rows()
            tk.Button(window.grids[title].button_frame, text='Отменить представления', command=delete_performances).pack(side='left', expand=True, anchor='w', padx=20)
            window.grids[title].button.pack(anchor='e')

        if title == 'Исполнитель':
            def select_performers():
                select_window = ChildWindow(window.window, 'Выберите спектакль', '300x75')
                _, data = db.select('SELECT Название FROM Спектакль')
                select_play = ttk.Combobox(select_window.element, values=[''] + [row[0] for row in data], width=40, state='readonly')
                select_play.pack(pady=10)
                def filt(play):
                    if not play:
                        play == 'NULL'
                    grid = window.grids['Исполнитель']
                    grid.QUERY = f"SELECT * FROM dbo.ИсполнителиСпектакля((SELECT ID FROM Спектакль WHERE Название = '{play}'))"
                    grid.update()
                    window.check_rows()
                tk.Button(select_window.element, text='Отфильтровать по спектаклю', command=lambda: filt(select_play.get())).pack()
            tk.Button(window.grids[title].button_frame, text='Выбрать конкретных исполнителей', command=select_performers).pack(side='left', expand=True, anchor='w', padx=20)
            window.grids[title].button.pack(anchor='e')
    window.start()

if __name__ == '__main__':
    __main__()