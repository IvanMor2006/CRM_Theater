import pyodbc

class Database:
    def __init__(self):
        self.connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\SQLEXPRESS01;'
            'DATABASE=Театр;'
            'Trusted_Connection=yes;'
            'Encrypt=yes;'
            'TrustServerCertificate=yes;'
        )
        conn = pyodbc.connect(self.connection_string)
        self.cursor = conn.cursor()

    def insert(self, table, fields, values):
        single = False
        if len(values) == 1:
            single = True
        values = str(values).replace("'NULL'", "NULL")
        if single:
            values = values[:-2] + values[-1:]
        query = f'INSERT INTO {table}({", ".join(fields)}) VALUES {values}'
        self.cursor.execute(query)
        self.cursor.commit()

    def update(self, table, fields, values, id):
        sets = []
        for f, v in zip(fields, values):
            if isinstance(v, str):
                v = '\'' + v + '\''
            sets.append(f'{f} = {v}')
        query = f'UPDATE {table} SET {", ".join(sets)} WHERE ID = {id}'
        self.cursor.execute(query)
        self.cursor.commit()

    def delete(self, table, id):
        query = f'DELETE FROM {table} WHERE ID IN ({", ".join(id)})'
        self.cursor.execute(query)
        self.cursor.commit()
        return id

    def select(self, text):
        self.cursor.execute(text)
        fields: tuple[str, type]
        fields = [(col[0], col[1]) for col in self.cursor.description]
        data = self.cursor.fetchall()
        return fields, data

db = Database()