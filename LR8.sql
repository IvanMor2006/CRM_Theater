/*
Лабораторная работа №5
«Создание таблиц с помощью языка SQL»
В отчёте должны быть операторы SQL для создания всех таблиц собственной базы данных.
Также в работе должны быть определены: одно значение поля по умолчанию, одно ограничение уникальности и одно проверочное
ограничение. Значение поля по умолчанию, ограничение уникальности и проверочное ограничение на таблицы с данными по
сотрудникам и должностям к рассмотрению не принимаются.
*/
ALTER TABLE Билет DROP CONSTRAINT FK_Билет_Представление
GO
ALTER TABLE Представление DROP CONSTRAINT FK_Представление_Зал
GO
ALTER TABLE Представление DROP CONSTRAINT FK_Представление_Спектакль
GO
ALTER TABLE Исполнитель DROP CONSTRAINT FK_Исполнитель_Сотрудник
GO
ALTER TABLE Исполнитель DROP CONSTRAINT FK_Исполнитель_Роль
GO
ALTER TABLE Роль DROP CONSTRAINT FK_Роль_Спектакль
GO
ALTER TABLE Спектакль DROP CONSTRAINT FK_Спектакль_Пьеса
GO
ALTER TABLE Спектакль DROP CONSTRAINT FK_Спектакль_Сотрудник
GO
ALTER TABLE Сотрудник DROP CONSTRAINT FK_Сотрудник_Должность
GO
ALTER TABLE Пьеса DROP CONSTRAINT FK_Пьеса_Жанр
GO

DROP TABLE Билет
GO
DROP TABLE Представление
GO
DROP TABLE Исполнитель
GO
DROP TABLE Роль
GO
DROP TABLE Спектакль
GO
DROP TABLE Зал
GO
DROP TABLE Сотрудник
GO
DROP TABLE Пьеса
GO
DROP TABLE Должность
GO
DROP TABLE Жанр
GO

CREATE TABLE Жанр (
  ID INT IDENTITY PRIMARY KEY,
  Название VARCHAR(40) NOT NULL
)
GO
CREATE TABLE Должность (
  ID INT IDENTITY PRIMARY KEY,
  Название VARCHAR(40) NOT NULL
)
GO
CREATE TABLE Пьеса (
  ID INT IDENTITY PRIMARY KEY,
  Название VARCHAR(40) NOT NULL,
  Автор VARCHAR(40) NOT NULL,
  IDЖанра INT NOT NULL
)
GO
CREATE TABLE Сотрудник (
  ID INT IDENTITY PRIMARY KEY,
  Фамилия VARCHAR(40) NOT NULL,
  Имя VARCHAR(40) NOT NULL,
  IDДолжности INT NOT NULL,
  Пол VARCHAR(40) NOT NULL DEFAULT 'Мужской',
  ДатаРождения DATE NOT NULL
)
GO
CREATE TABLE Зал (
  ID INT IDENTITY PRIMARY KEY,
  Название VARCHAR(40) NOT NULL,
  Вместимость INT NOT NULL DEFAULT 250
)
GO
CREATE TABLE Спектакль (
  ID INT IDENTITY PRIMARY KEY,
  Название VARCHAR(40) NOT NULL,
  IDРежиссёра INT NOT NULL,
  ДатаПремьеры DATETIME,
  IDПьесы INT
)
GO
CREATE TABLE Роль (
  ID INT IDENTITY PRIMARY KEY,
  Название VARCHAR(40) NOT NULL,
  IDСпектакля INT NOT NULL
)
GO
CREATE TABLE Исполнитель (
  ID INT IDENTITY PRIMARY KEY,
  IDРоли INT NOT NULL,
  IDСотрудника INT NOT NULL,
  ДатаНазначения DATE NOT NULL,
  ДатаСнятия DATE,
  CONSTRAINT СнятиеПозжеНазначения CHECK (ДатаСнятия > ДатаНазначения)
)
GO
CREATE TABLE Представление (
  ID INT IDENTITY PRIMARY KEY,
  IDСпектакля INT NOT NULL,
  IDЗала INT NOT NULL,
  Дата DATETIME NOT NULL,
  CONSTRAINT УникальныеЗалДата UNIQUE (IDЗала, Дата)
)
GO
CREATE TABLE Билет (
  ID INT IDENTITY PRIMARY KEY,
  Ряд INT,
  Место INT NOT NULL,
  Цена MONEY NOT NULL DEFAULT 15.00,
  ДатаПродажи DATETIME NOT NULL DEFAULT GETDATE(),
  IDПредставления INT NOT NULL
)
GO

/*
Лабораторная работа №7
«Определение связей между таблицами с помощью языка SQL»
В отчёте должны быть операторы SQL для определения всех связей между таблицами собственной базы данных (Alter Table + CONSTRAINT).
Также в Alter Table должны быть определены: одно ограничение уникальности и одно проверочное ограничение.Ограничение 
уникальности и проверочное ограничение на таблицы с данными по сотрудникам и должностям к рассмотрениюне принимаются.
*/
ALTER TABLE Пьеса
  ADD CONSTRAINT FK_Пьеса_Жанр
        FOREIGN KEY (IDЖанра) REFERENCES Жанр(ID)
GO
ALTER TABLE Сотрудник
  ADD CONSTRAINT FK_Сотрудник_Должность
        FOREIGN KEY (IDДолжности) REFERENCES Должность(ID)
GO
ALTER TABLE Спектакль
  ADD CONSTRAINT FK_Спектакль_Сотрудник
        FOREIGN KEY (IDРежиссёра) REFERENCES Сотрудник(ID),
      CONSTRAINT FK_Спектакль_Пьеса
        FOREIGN KEY (IDПьесы) REFERENCES Пьеса(ID)
GO
ALTER TABLE Роль
  ADD CONSTRAINT FK_Роль_Спектакль
        FOREIGN KEY (IDСпектакля) REFERENCES Спектакль(ID)
GO
ALTER TABLE Исполнитель
  ADD CONSTRAINT FK_Исполнитель_Роль
        FOREIGN KEY (IDРоли) REFERENCES Роль(ID),
      CONSTRAINT FK_Исполнитель_Сотрудник
        FOREIGN KEY (IDСотрудника) REFERENCES Сотрудник(ID)
GO
ALTER TABLE Представление
  ADD CONSTRAINT FK_Представление_Спектакль
        FOREIGN KEY (IDСпектакля) REFERENCES Спектакль(ID),
      CONSTRAINT FK_Представление_Зал
        FOREIGN KEY (IDЗала) REFERENCES Зал(ID)
GO
ALTER TABLE Билет
  ADD CONSTRAINT FK_Билет_Представление
        FOREIGN KEY (IDПредставления) REFERENCES Представление(ID),
      CONSTRAINT УникальныеРядМестоПредставление
        UNIQUE (Ряд, Место, IDПредставления),
      CONSTRAINT ЦенаНеОтрицательная
        CHECK (Цена >= 0)
GO

/*
Лабораторная работа №8
«Использование языка SQL для заполнения базы данных»
В отчёте должны быть операторы SQL для занесения данных в собственную базу данных – INSERT INTO…VALUES.
В результате выполнения работы:
1)      в каждую таблицу должно быть занесено не менее 5-ти записей;
2)      в каждую дочернюю таблицу должно быть занесено больше записей, чем в любую из её родительских таблиц.
*/
INSERT INTO Жанр(Название)
  VALUES ('Комедия'),
         ('Трагедия'),
         ('Трагикомедия'),
         ('Боевик'),
         ('Фантастика')
INSERT INTO Должность(Название)
  VALUES ('Актёр'),
         ('Режиссёр'),
         ('Кассир'),
         ('Гримёр'),
         ('Костюмер')
INSERT INTO Пьеса(Название, Автор, IDЖанра)
  VALUES ('Маленький принц', 'Чехов А. П.', 3),
         ('Собачье сердце', 'Булгаков М. А.', 4),
         ('Дикая охота короля Стаха', 'Короткевич В. С.', 4),
         ('Ринг. Драма. Жизнь.', 'Андрушко А.', 1),
         ('METRO 2033', 'Будейко А.', 1),
         ('Звёздные войны', 'Будейко А.', 2)
INSERT INTO Сотрудник(Фамилия, Имя, IDДолжности, Пол, ДатаРождения)
  VALUES ('Будейко', 'Андрей', 2, 'Мужской', '19970813'),
         ('Андрушко', 'Александр', 2, 'Мужской', '20000208'),
         ('Морозов', 'Иван', 1, 'Мужской', '20060413'),
         ('Шаповалова', 'Виктория', 1, 'Женский', '20070625'),
         ('Соболевская', 'Мария', 4, 'Женский', '20070204'),
         ('Мустафин', 'Игорь', 3, 'Мужской', '20010904')
INSERT INTO Зал(Название, Вместимость)
  VALUES ('Сцена', 50),
         ('Малый зал', 100),
         ('Средний зал', 200),
         ('Большой зал', 300),
         ('Кукольный зал', 120)
INSERT INTO Спектакль(Название, IDРежиссёра, ДатаПремьеры, IDПьесы)
  VALUES ('Ринг. Драма. Жизнь.', 2, '20250616', 4),
         ('Метро', 1, '20220226', 5),
         ('Звёздные войны', 1, '20240808', 6),
         ('Собачье сердце', 2, '20200314', 3),
         ('Дикая охота короля Стаха', 2, '20250709', 3),
         ('Маленький принц и планета безопасности', 1, '20180404', 1),
         ('Маленький принц', 1, '20150714', 1)
INSERT INTO Роль(Название, IDСпектакля)
  VALUES ('Икар', 3),
         ('Полковник Мельников', 2),
         ('Детектив', 5),
         ('Маленький принц', 7),
         ('Адриан Стакатте', 1),
         ('Тим', 2),
         ('Девочка', 2),
         ('Младшая дочь', 3)
INSERT INTO Исполнитель(IDРоли, IDСотрудника, ДатаНазначения, ДатаСнятия)
  VALUES (1, 3, '20230906', NULL),
         (2, 1, '20220919', NULL),
         (3, 2, '20250505', '20250901'),
         (4, 3, '20150413', '20160413'),
         (5, 1, '20250112', NULL),
         (6, 3, '20220919', NULL),
         (7, 4, '20220919', '20240901'),
         (8, 4, '20230906', '20240901'),
         (3, 6, '20250901', NULL)
INSERT INTO Представление(IDСпектакля, IDЗала, Дата)
  VALUES (1, 2, '20250617'),
         (5, 3, '20250713'),
         (6, 1, '20220226'),
         (7, 4, '20150714'),
         (3, 2, '20240807'),
         (4, 4, '20250319'),
         (3, 2, '20240808'),
         (1, 4, '20210602')
INSERT INTO Билет(Ряд, Место, Цена, ДатаПродажи, IDПредставления)
  VALUES (3, 14, 10.00, '20200315', 7),
         (3, 13, 7.29, '20200315', 7),
         (3, 12, 7.00, '20240801', 7),
         (8, 9, 5.00, '20150702', 4),
         (1, 10, 15.00, '20150715', 6),
         (4, 1, 12.00, '20250626', 1),
         (2, 3, 8.00, '20250610', 2),
         (NULL, 44, 10.00, '20220220', 3),
         (NULL, 12, 10.00, '20220202', 5)
GO

DROP TABLE БилетLog
GO

CREATE TABLE БилетLog(
  ID INT IDENTITY PRIMARY KEY,
  typelog CHAR NOT NULL,
  datelog DATETIME NOT NULL,
  userlog VARCHAR(100),
  hostlog VARCHAR(100),

  IDБилета INT NOT NULL,
  Ряд INT,
  Место INT,
  Цена MONEY,
  ДатаПродажи DATETIME,
  IDПредставления INT
)
GO

CREATE TRIGGER trgБилетI ON Билет
  AFTER INSERT, UPDATE, DELETE
AS
DECLARE @datelog DATETIME = GETDATE()
INSERT INTO БилетLog
  SELECT 'D', @datelog, SYSTEM_USER, HOST_NAME(),
         NULL, Ряд, Место, Цена, ДатаПродажи, IDПредставления
    FROM deleted
INSERT INTO БилетLog
  SELECT 'I', @datelog, SYSTEM_USER, HOST_NAME(),
         ID, Ряд, Место, Цена, ДатаПродажи, IDПредставления
    FROM inserted
GO

DROP VIEW Билеты
GO
CREATE VIEW Билеты
AS
SELECT Б.ID, Б.Ряд, Б.Место, Б.Цена, Б.ДатаПродажи, CONCAT(FORMAT(П.Дата, 'yyyy-MM-dd HH:mm:ss'), ' - ', С.Название, ' - ', З.Название) Представление
  FROM Билет Б
       INNER JOIN Представление П ON Б.IDПредставления = П.ID
       INNER JOIN Спектакль С ON П.IDСпектакля = С.ID
       INNER JOIN Зал З ON П.IDЗала = З.ID
GO

DROP VIEW Представления
GO
CREATE VIEW Представления
AS
SELECT П.ID, С.Название Спектакль, З.Название Зал, П.Дата
  FROM Представление П
       INNER JOIN Спектакль С ON П.IDСпектакля = С.ID
       INNER JOIN Зал З ON П.IDЗала = З.ID
GO

DROP VIEW Спектакли
GO
CREATE VIEW Спектакли
AS
SELECT Сп.ID, Сп.Название, С.Фамилия Режиссёр, Сп.ДатаПремьеры, П.Название Пьеса
  FROM Спектакль Сп
       INNER JOIN Сотрудник С ON Сп.IDРежиссёра = С.ID
       LEFT JOIN Пьеса П ON Сп.IDПьесы = П.ID
GO

DROP VIEW Роли
GO
CREATE VIEW Роли
AS
SELECT Р.ID, Р.Название, С.Название Спектакль
  FROM Роль Р
       INNER JOIN Спектакль С ON Р.IDСпектакля = С.ID
GO

DROP VIEW Исполнители
GO
CREATE VIEW Исполнители
AS
SELECT И.ID, Р.Название Роль, С.Фамилия + ' ' + С.Имя Сотрудник, И.ДатаНазначения, И.ДатаСнятия
  FROM Исполнитель И
       INNER JOIN Роль Р ON И.IDРоли = Р.ID
       INNER JOIN Сотрудник С ON И.IDСотрудника = С.ID
GO

DROP VIEW Сотрудники
GO
CREATE VIEW Сотрудники
AS
SELECT С.ID, С.Фамилия, С.Имя, Д.Название Должность, С.Пол, С.ДатаРождения
  FROM Сотрудник С
       INNER JOIN Должность Д ON С.IDДолжности = Д.ID
GO

DROP VIEW Пьесы
GO
CREATE VIEW Пьесы
AS
SELECT П.ID, П.Название, П.Автор, Ж.Название Жанр
  FROM Пьеса П
       INNER JOIN Жанр Ж ON П.IDЖанра = Ж.ID
GO