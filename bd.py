import sqlite3
import os.path


class Student:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'accountant.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def __init__(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.__class__.__name__} ({self.__class__.__name__.lower()}_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, middle_name TEXT, last_name TEXT NOT NULL)")

    def create(self, name):
        if len(name.split()) == 3:
            f, m, l, = list(map(str.capitalize, name.split()))
            if len(self.cursor.execute(f"SELECT ({self.__class__.__name__.lower()}_id) FROM {self.__class__.__name__} WHERE first_name || middle_name || last_name == '{''.join(list(map(str.capitalize, name.split())))}' ").fetchall()) == 0:
                self.cursor.execute(f"INSERT OR IGNORE INTO {self.__class__.__name__} (first_name, middle_name, last_name) VALUES (?, ?, ?)", (f, m, l))
                print(f"Пользователь {name} добавлен")
                return self.conn.commit()
            else:
                print(f'{name} уже есть в БД')
        else:
            print('Ф.И.О введено не корректно')

    def read(self, name=None):
        if name:
            table = table = self.cursor.execute(f"SELECT first_name, middle_name, last_name, {self.__class__.__name__.lower()}_id FROM {self.__class__.__name__} WHERE first_name || middle_name || last_name == '{''.join(list(map(str.capitalize, name.split())))}'").fetchall()
        else:
            table = self.cursor.execute(f"SELECT first_name, middle_name, last_name, {self.__class__.__name__.lower()}_id FROM {self.__class__.__name__}").fetchall()

        count = 1
        for el in table:
            print(f'{count}.{el[0]} {el[1]} {el[2]} id:{el[3]}')
            count += 1

    def update(self, id_record, name):
        if len(name.split()) == 3:
            f, m, l, = list(map(str.capitalize, name.split()))
            self.cursor.execute(f"UPDATE {self.__class__.__name__} SET first_name = '{f}', middle_name = '{m}', last_name = '{l}'  WHERE {self.__class__.__name__.lower()}_id == {id_record} ")
            print(f"Запись с id:{id_record} обновлена")
            return self.conn.commit()

    def delete(self, id_record):
        student_id = self.cursor.execute(f"SELECT {self.__class__.__name__.lower()}_id FROM {self.__class__.__name__} WHERE {self.__class__.__name__.lower()}_id == {id_record}").fetchall()
        sg_id = self.cursor.execute(f"SELECT studgroup_id FROM StudGroup WHERE student_fk == {id_record}").fetchall()
        if len(sg_id) > 0:
            pt = StudGroup()
            pt.delete(sg_id[0][0])

        if len(student_id) > 0:
            self.cursor.execute(f"DELETE FROM {self.__class__.__name__} WHERE {self.__class__.__name__.lower()}_id == {id_record}")
            print(f'Пользователь с id:{id_record} удалён')
            return self.conn.commit()
        else:
            print(f'Пользователя с {id_record} нет в БД')


class StudGroup:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'accountant.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def __init__(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.__class__.__name__} ({self.__class__.__name__.lower()}_id INTEGER PRIMARY KEY AUTOINCREMENT, student_fk INTEGER, first_name TEXT NOT NULL, middle_name TEXT, last_name TEXT NOT NULL, group_number INTEGER NOT NULL, FOREIGN KEY (student_fk) REFERENCES Student (student_id))")

    def create(self, name, group_number):
        if len(name.split()) == 3:
            f, m, l, = list(map(str.capitalize, name.split()))
            try:
                student_id = self.cursor.execute(f"SELECT student_id FROM Student WHERE first_name || middle_name || last_name == '{''.join(list(map(str.capitalize, name.split())))}'").fetchall()
                student_fk = self.cursor.execute(f"SELECT student_fk FROM {self.__class__.__name__} WHERE student_fk == {student_id[0][0]}").fetchall()
                if len(student_fk) == 0:
                    self.cursor.execute(f"INSERT OR IGNORE INTO {self.__class__.__name__} (student_fk, first_name, middle_name, last_name, group_number) VALUES (?, ?, ?, ?, ?)", (student_id[0][0], f, m, l, group_number))
                    print(f'Студент {name} добавлен в группу №{group_number}')
                    return self.conn.commit()
                else:
                    print(f'Студент {name} уже состоит в группе')
            except Exception:
                print(f'{name} не сохранён в БД')
        else:
            print(f'{name} Ф.И.О введено не корректно')

    def read(self, group_number=None):
        if group_number:
            table = self.cursor.execute(
                f"SELECT first_name, middle_name, last_name, group_number, {self.__class__.__name__.lower()}_id FROM {self.__class__.__name__} WHERE group_number == {group_number}").fetchall()
        else:
            table = self.cursor.execute(
                f"SELECT first_name, middle_name, last_name, group_number, {self.__class__.__name__.lower()}_id FROM {self.__class__.__name__}").fetchall()

        count = 1
        for el in table:
            print(f'{count}.{el[0]} {el[1]} {el[2]} гр.№{el[3]} id:{el[4]}')
            count += 1

    def update(self, id_record, group_number):
        self.cursor.execute(f"UPDATE {self.__class__.__name__} SET group_number = '{group_number}' WHERE {self.__class__.__name__.lower()}_id == {id_record} ")
        return self.conn.commit()

    def delete(self, id_record):
        self.cursor.execute(f"DELETE FROM {self.__class__.__name__} WHERE {self.__class__.__name__.lower()}_id == {id_record}")
        return self.conn.commit()


class Teacher(Student):

    def delete(self, id_record):
        teacher_id = self.cursor.execute(f"SELECT {self.__class__.__name__.lower()}_id FROM {self.__class__.__name__} WHERE {self.__class__.__name__.lower()}_id == {id_record}").fetchall()
        subject_id = self.cursor.execute(f"SELECT subject_id FROM Subject WHERE teacher_fk == {id_record}").fetchall()
        if len(subject_id) > 0:
            pt = Subject()
            pt.delete(subject_id[0][0])

        if len(teacher_id) > 0:
            self.cursor.execute(f"DELETE FROM {self.__class__.__name__} WHERE {self.__class__.__name__.lower()}_id == {id_record}")
            print(f'Пользователь с id:{id_record} удалён')
            return self.conn.commit()
        else:
            return f'Пользователя с {id_record} нет в БД'


class Subject:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'accountant.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def __init__(self):
        super().__init__()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.__class__.__name__} (subject_id INTEGER PRIMARY KEY AUTOINCREMENT, teacher_fk INTEGER, first_name TEXT NOT NULL, middle_name TEXT, last_name TEXT NOT NULL, subject TEXT NOT NULL, FOREIGN KEY (teacher_fk) REFERENCES Teacher (teacher_id))")

    def create(self, name, subject):
        if len(name.split()) == 3:
            f, m, l, = list(map(str.capitalize, name.split()))
            try:
                teacher_id = self.cursor.execute(f"SELECT teacher_id FROM Teacher WHERE first_name || middle_name || last_name == '{''.join(list(map(str.capitalize, name.split())))}'").fetchall()
                teacher_fk = self.cursor.execute(f"SELECT teacher_fk FROM {self.__class__.__name__} WHERE teacher_fk == {teacher_id[0][0]}").fetchall()
                if len(teacher_fk) == 0:
                    self.cursor.execute(f"INSERT OR IGNORE INTO {self.__class__.__name__} (teacher_fk, first_name, middle_name, last_name, subject) VALUES (?, ?, ?, ?, ?)", (teacher_id[0][0], f, m, l, subject))
                    print(f"Предмет {subject} добавлен {name}")
                    return self.conn.commit()
                else:
                    print(f'У {name} уже есть предмет')
            except Exception:
                print(f'{name} не сохранён в БД')
        else:
            print(f'{name} Ф.И.О введено не корректно')

    def read(self, subject=None):
        if subject:
            table = self.cursor.execute(
                f"SELECT first_name, middle_name, last_name, subject, {self.__class__.__name__.lower()}_id FROM {self.__class__.__name__} WHERE subject == '{subject}'").fetchall()
        else:
            table = self.cursor.execute(
                f"SELECT first_name, middle_name, last_name, subject, {self.__class__.__name__.lower()}_id FROM {self.__class__.__name__}").fetchall()

        count = 1
        for el in table:
            print(f'{count}.{el[0]} {el[1]} {el[2]} предмет: {el[3]} id:{el[4]}')
            count += 1

    def update(self, id_record, subject):
        self.cursor.execute(f"UPDATE {self.__class__.__name__} SET subject = '{subject}' WHERE {self.__class__.__name__.lower()}_id == {id_record} ")
        return self.conn.commit()

    def delete(self, id_record):
        self.cursor.execute(f"DELETE FROM {self.__class__.__name__} WHERE {self.__class__.__name__.lower()}_id == {id_record}")
        return self.conn.commit()



