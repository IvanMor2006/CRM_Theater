import tkinter as tk
from tkinter import messagebox

from database import db
from grid import Grid

class Menu:
    def __init__(self, parent):
        self.parent = parent
        self.element = tk.Menu(self.parent.window)
        self.parent.window.config(menu=self.element)

        self.element.add_command(label='Log билетов', command=self.__log)

    def __log(self):
        query = '''
            SELECT Б.ID, typelog, datelog, userlog, hostlog,
                   IDБилета, Ряд, Место, Цена, ДатаПродажи, CONCAT(С.Название, ' - ', З.Название, ' (', FORMAT(П.Дата, 'yyyy-MM-dd HH:mm:ss'), ')') Представление
              FROM БилетLog Б
                   INNER JOIN Представление П ON Б.IDПредставления = П.ID
                   INNER JOIN Спектакль С ON П.IDСпектакля = С.ID
                   INNER JOIN Зал З ON П.IDЗала = З.ID
        '''
        log_window = tk.Toplevel(self.parent.window)
        log_window.title('Билеты Log')
        size = '1200x600'
        log_window.geometry(size)
        width, height = size.split('x')
        log_window.geometry(f'+{log_window.winfo_screenwidth() // 2 - int(width) // 2}+{log_window.winfo_screenheight() // 2 - int(height) // 2}')
        log_window.transient(self.parent.window)
        log_window.grab_set()
        frame = tk.Frame(log_window)
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        grid = Grid(frame, query + 'ORDER BY datelog DESC, ID DESC', False)