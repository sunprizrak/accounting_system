import click
from bd import *


@click.command()
@click.argument('table_name')
@click.argument('method')
@click.option('--name', '-n', type=str, help='Ф.И.О студента')
@click.option('--i_d', '-id', type=int, help='id записи')
@click.option('--group_num', '-g', type=int, help='№ группы')
@click.option('--subject', '-s', type=str, help='Предмет')
def main(table_name, method, name, i_d, group_num, subject):
    """ <table_name.method(options)> ; \n
        table_name : student, teacher, group, subject ; \n
        method: create, read, update, delete ; /n
        <student.create(name)>, <student.read() or student.read(name)>, <student.update(i_d, name)>, <student.delete(i_d)> ; \n
        <teacher.create(name)>, <teacher.read() or teacher.read(name)>, <teacher.update(i_d, name)>, <teacher.delete(i_d)> ; \n
        <group.create(name, group_num)>, <group.read() or group.read(group_num)>, <group.update(i_d, group_num)>, <group.delete(i_d)> ; \n
        <subject.create(name, subject)>, <subject.read() or subject.read(subject)>, <subject.update(i_d, subject)>, <subject.delete(i_d)> ;
    """

    if table_name.lower() in ['student', 'teacher']:
        pt = Student() if table_name.lower() == 'student' else Teacher()
        if method.lower() == 'create':
            if name:
                pt.create(name)
            else:
                print('Не указано имя')
        elif method.lower() == 'read':
            if name:
                pt.read(name)
            else:
                pt.read()
        elif method.lower() == 'update':
            if i_d and name:
                pt.update(i_d, name)
            else:
                print('Укажите i_d и имя')
        elif method.lower() == 'delete':
            if i_d:
                pt.delete(i_d)
            else:
                print('Не уазан id удаляемой записи')
    elif table_name.lower() == 'group':
        pt = StudGroup()
        if method.lower() == 'create':
            if name and group_num:
                pt.create(name, group_num)
            else:
                print('Укажите имя студента и номер группы')
        elif method.lower() == 'read':
            if group_num:
                pt.read(group_num)
            else:
                pt.read()
        elif method.lower() == 'update':
            if i_d and group_num:
                pt.update(i_d, group_num)
            else:
                print('Укажите id студента и номре группы')
        elif method.lower() == 'delete':
            if i_d:
                pt.delete(i_d)
            else:
                print('Укажите id записи')
    elif table_name.lower() == 'subject':
        pt = Subject()
        if method.lower() == 'create':
            if name and subject:
                pt.create(name, subject)
            else:
                print('Укажите имя учителя и предмет')
        elif method.lower() == 'read':
            if subject:
                pt.read(subject)
            else:
                pt.read()
        elif method.lower() == 'update':
            if i_d and subject:
                pt.update(i_d, subject)
            else:
                print('Укажите id учителя и предмет')
        elif method.lower() == 'delete':
            if i_d:
                pt.delete(i_d)
            else:
                print('Укажите id записи')


if __name__ == '__main__':
    main()