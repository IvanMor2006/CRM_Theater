from datetime import datetime

TABLES = {
    'Билет': {
        'IDTable': 'IDБилета',
        'size': '700x460',
        'query': '''
            SELECT * FROM Билеты
              ORDER BY Представление DESC, Ряд, Место
        '''
    },
    'Представление': {
        'IDTable': 'IDПредставления',
        'size': '700x670',
        'query': '''
            SELECT * FROM Представления
              ORDER BY Дата DESC, Зал
        '''
    },
    'Спектакль': {
        'IDTable': 'IDСпектакля',
        'size': '700x700',
        'query': '''
            SELECT * FROM Спектакли
              ORDER BY ДатаПремьеры DESC
        '''
    },
    'Зал': {
        'IDTable': 'IDЗала',
        'size': '310x100',
        'query': '''
            SELECT * FROM Зал
              ORDER BY Вместимость
        '''
    },
    'Роль': {
        'IDTable': 'IDроли',
        'size': '700x370',
        'query': '''
            SELECT * FROM Роли
              ORDER BY Спектакль, Название
        '''
    },
    'Исполнитель': {
        'IDTable': 'IDИсполнителя',
        'size': '700x700',
        'query': '''
            SELECT * FROM Исполнители
              ORDER BY Сотрудник, Роль, ДатаНазначения DESC
        '''
    },
    'Сотрудник': {
        'IDTable': 'IDСотрудника',
        'size': '330x460',
        'query': '''
            SELECT * FROM Сотрудники
              ORDER BY Должность, Фамилия, Имя
        '''
    },
    'Режиссёр': {
        'IDTable': 'IDРежиссёра',
        'query': '''
            SELECT * FROM Сотрудники
              WHERE Должность = 'Режиссёр'
              ORDER BY Должность, Фамилия, Имя
        '''
    },
    'Должность': {
        'IDTable': 'IDДолжности',
        'size': '300x70',
        'query': '''
            SELECT * FROM Должность
              ORDER BY Название
        '''
    },
    'Пьеса': {
        'IDTable': 'IDПьесы',
        'size': '300x400',
        'query': '''
            SELECT * FROM Пьесы
              ORDER BY Автор, Название
        '''
    },
    'Жанр': {
        'IDTable': 'IDЖанра',
        'size': '300x70',
        'query': '''
            SELECT * FROM Жанр
              ORDER BY Название
        '''
    }
}

CONSTRAINTS = {
    'УникальныеРядМестоПредставление': 'Не может быть на одном представлении 2 билета на одно и то же место!',
    'ЦенаНеОтрицательная': 'Цена не может быть отрицательной!',
    'СнятиеПозжеНазначения': 'Снятие с роли должно быть позже назначения!',
    'УникальныеЗалДата': 'Не может быть 2 представления в одно и то же время в одном зале!'
}

NULL_FIELDS = {'Ряд', 'Цена', 'ДатаСнятия', 'ДатаПремьеры', 'IDПьесы'}
DEFUALT_FIELDS = {
    'Цена': 15.00,
    'Пол': 'Мужской',
    'Вместимость': 250,
    'ДатаПродажи': lambda: datetime.now().replace(microsecond=0)
}

def __main__():
    pass

if __name__ == '__main__':
    __main__()