from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from grid import Grid
from child_window import ChildWindow
from report import Report
from database import db

class Menu:
    def __init__(self, parent):
        self.parent = parent
        self.element = tk.Menu(self.parent.window)
        self.parent.window.config(menu=self.element)

        reports = tk.Menu(self.element, tearoff=0)
        reports.add_command(label='Открытая таблица на данный момент', command=self.__report_table)
        reports.add_command(label='Итоги цен билетов', command=lambda: self.__report(
            '''SELECT AVG(Цена) СредняяЦена, MIN(Цена) МинимальнаяЦена, MAX(Цена) МаксимальнаяЦена
                 FROM Билет''',
            'Итоги цен'))
        reports.add_command(label='Выручка за представления', command=lambda: self.__report(
            'SELECT * FROM ВыручкаПоПредставлениям',
            'Выручка'))
        reports.add_command(label='Загрузка залов', command=lambda: self.__report(
            'SELECT * FROM ЗаполнениеЗалов',
            'Загрузка залов'))
        reports.add_command(label='Представления в заданную дату', command=self.__report_performances)
        self.element.add_cascade(label='Отчёты', menu=reports)

        self.element.add_command(label='Log билетов', command=self.__log)
        self.element.add_command(label='Поиск', command=self.__search)
        self.element.add_command(label='Фильтрация')

    def __report_table(self):
        table = self.parent.notebook.tab('current', 'text')
        grid = self.parent.grids[table]
        exporter = Report(self.parent.window, grid, table)
        exporter.export()
    def __report(self, query, filename):
        exporter = Report(self.parent.window, query, filename)
        exporter.export(first_col=True)
    def __report_performances(self):
        report_window = ChildWindow(self.parent.window, 'Выберите дату', '300x200')
        report_window.element.grab_release()
        tk.Label(report_window.element, text='Год').pack()
        year = ttk.Spinbox(report_window.element, from_=2000, to=datetime.now().year, wrap=True)
        year.pack(pady=5)
        year.focus()
        months = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        for i, month in enumerate(months, 0):
            if i:
                months[i] = str(i) + ' ' + month
        tk.Label(report_window.element, text='Месяц').pack()
        month = ttk.Combobox(report_window.element, values=months, state='readonly')
        month.current(0)
        month.pack(pady=5)
        tk.Label(report_window.element, text='День').pack()
        day = ttk.Spinbox(report_window.element, from_=1, to=31, wrap=True)
        day.pack(pady=5)
        def report_date(year, month, day):
            title = f'Представления за{year}-{month[2:]}-{day}'
            if not year:
                year = 'NULL'
            if not (month and (month := int(month[0]))):
                month = 'NULL'
            if not day:
                day = 'NULL'
            exporter = Report(report_window.element, f'SELECT * FROM ПредставленияВЗаданнуюДату({year}, {month}, {day})', title)
            if exporter.export():
                report_window.element.destroy()
        tk.Button(report_window.element, text='Сделать отчёт', command=lambda: report_date(year.get(), month.get(), day.get())).pack()

    def __log(self):
        query = '''
            SELECT Б.ID, typelog, datelog, userlog, hostlog,
                   IDБилета, Ряд, Место, Цена, ДатаПродажи, CONCAT(С.Название, ' - ', З.Название, ' (', FORMAT(П.Дата, 'yyyy-MM-dd HH:mm:ss'), ')') Представление
              FROM БилетLog Б
                   INNER JOIN Представление П ON Б.IDПредставления = П.ID
                   INNER JOIN Спектакль С ON П.IDСпектакля = С.ID
                   INNER JOIN Зал З ON П.IDЗала = З.ID
              ORDER BY datelog DESC, ID DESC
        '''
        log_window = ChildWindow(self.parent.window, 'Log Билетов')
        log_window.element.focus()
        grid = Grid(log_window.element, query, False)
        grid.frame.pack(padx=10, pady=10, side='top', fill='both', expand=True)

    def __search(self):
        search_window = ChildWindow(self.parent.window, 'Поиск', '300x100')
        search_window.element.grab_release()

        frame = tk.Frame(search_window.element)
        tk.Label(frame, text='Введите значения для поиска').pack()
        value = tk.StringVar()
        entry = tk.Entry(frame, width=40, textvariable=value)
        entry.focus()
        entry.pack()
        frame.pack(pady=10)

        search_window.table = self.parent.notebook.tab('current', 'text')
        search_window.grid = self.parent.grids[search_window.table]
        def s():
            for row in search_window.grid.rows:
                for elem in row[1:]:
                    if value.get() in str(elem):
                        yield row[0]
                        break
        search_window.gen = s()

        def get_next():
            try:
                new_table = self.parent.notebook.tab('current', 'text')
                if new_table != search_window.table:
                    search_window.table = new_table
                    search_window.grid = self.parent.grids[search_window.table]
                    search_window.gen = s()

                search_window.grid.select_row_by_id(next(search_window.gen))
            except StopIteration:
                messagebox.showinfo('Поиск' , 'Достигнут конец таблицы. Возвращение в начало', parent=search_window.element)
                search_window.gen = s()
                try:
                    search_window.grid.select_row_by_id(next(search_window.gen))
                except:
                    pass

        button = tk.Button(search_window.element, text='Поиск', command=get_next)
        button.pack()
        entry.bind('<Return>', lambda event: button.invoke())