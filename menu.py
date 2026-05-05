from datetime import datetime
import tkinter as tk
from tkinter import ttk

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
            'ИтогиЦен'))
        reports.add_command(label='Выручка за представления', command=lambda: self.__report(
            'SELECT * FROM ВыручкаПоПредставлениям',
            'Выручка'))
        reports.add_command(label='Загрузка залов', command=lambda: self.__report(
            'SELECT * FROM ЗаполнениеЗалов',
            'ЗагрузкаЗалов'))
        reports.add_command(label='Представления в заданную дату', command=self.__report_performances)
        self.element.add_cascade(label='Отчёты', menu=reports)

        self.element.add_command(label='Log билетов', command=self.__log)
        self.element.add_command(label='Log билетов', command=self.__log)

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
        grid = Grid(log_window.element, query, False)
        grid.frame.pack(padx=10, pady=10, side='top', fill='both', expand=True)

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
        tk.Label(report_window.element, text='Год').pack()
        year = ttk.Spinbox(report_window.element, from_=2000, to=datetime.now().year, wrap=True)
        year.pack(pady=5)
        months = {}
        for i, month in enumerate(['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'], 0):
            months[month] = i
        tk.Label(report_window.element, text='Месяц').pack()
        month = ttk.Combobox(report_window.element, values=list(months.keys()), state='readonly')
        month.current(0)
        month.pack(pady=5)
        tk.Label(report_window.element, text='День').pack()
        day = ttk.Spinbox(report_window.element, from_=1, to=31, wrap=True)
        day.pack(pady=5)
        def __report_date(year, month, day):
            title = f'ПредставленияЗа{year}-{month if month else ""}-{day}'
            if not year:
                year = 'NULL'
            if not month:
                month = 'NULL'
            if not day:
                day = 'NULL'
            exporter = Report(report_window.element, f'SELECT * FROM ПредставленияВЗаданнуюДату({year}, {month}, {day})', title)
            if exporter.export():
                report_window.element.destroy()
        tk.Button(report_window.element, text='Сделать отчёт', command=lambda: __report_date(year.get(), months[month.get()], day.get())).pack()