import sqlite3
from random import randint


class LoginAlreadyExists(Exception):
    pass


class InvalidLogin(Exception):
    pass


class InvalidPassword(Exception):
    pass


class UnexpectedError(Exception):
    pass


class ShortPassword(Exception):
    pass


class InvalidChars(Exception):
    pass


class PasswordsNotMatch(Exception):
    pass


def get_id():
    return randint(10000, 200000)


class Profile:
    def __init__(self, login, password, password_ok=None):
        self.login = login
        self.password = password
        self.id = get_id()
        if password_ok != None and password != password_ok:
            raise PasswordsNotMatch('Пароли не совпадают!')

    def check_password(self):
        if len(self.password) < 8:
            raise ShortPassword('Пароль должен содержать хотя бы 8 символов!')
        flag = True
        for char in self.password:
            if char.isdigit():
                flag = False
        if flag:
            raise InvalidChars('Пароль должен содержать хотя бы одну цифру!')

    def add_to_base(self):
        try:
            con = sqlite3.connect("base.sqlite")
            cur = con.cursor()

            # Выполнение запроса и получение всех результатов
            cur.execute('''INSERT INTO profile VALUES (?, ?, ?) ''', (self.id, self.login, self.password))
            con.commit()

            con.close()
        except sqlite3.IntegrityError:
            raise LoginAlreadyExists('Логин занят!')


class Session:
    def __init__(self, id_session, id_profile):
        self.id_session = id_session
        self.id_profile = id_profile

    def add_to_base(self, time, num=1):

        try:
            con = sqlite3.connect("base.sqlite")
            cur = con.cursor()

            cur.execute('''INSERT INTO sessions VALUES (?, ?, ?, ?) ''',
                        (self.id_profile, self.id_session, num, time))
            con.commit()

            con.close()
        except:
            raise UnexpectedError('Непредвиденная ошибка')


def get_all_sessions():
    res = ''
    try:
        con = sqlite3.connect("base.sqlite")
        cur = con.cursor()

        cur.execute('''SELECT * FROM sessions''')
        res = cur.fetchall()
    except:
        raise UnexpectedError('Непредвиденная ошибка')
    return res


def get_all_profiles():
    res = ''
    try:
        con = sqlite3.connect("base.sqlite")
        cur = con.cursor()

        cur.execute('''SELECT * FROM profile''')
        res = cur.fetchall()
    except:
        raise UnexpectedError('Непредвиденная ошибка')
    return res


def authorization(login, password):
    profiles = get_all_profiles()
    for profile in profiles:
        if profile[1] == login:
            if profile[2] == password:
                return profile[0]
            else:
                raise InvalidPassword('Неверный пароль!')
    raise InvalidLogin('Неверный логин!')


def change_password(login, password, new_password):
    if authorization(login, password):
        Profile(login, new_password).check_password()
        try:
            con = sqlite3.connect("base.sqlite")
            cur = con.cursor()

            cur.execute(f'UPDATE profile SET password = ? WHERE login = ?', (new_password, login))
            con.commit()

            con.close()
        except:
            raise UnexpectedError('Непредвиденная ошибка')


def get_profile(login=None, password=None, id=None):
    res = ''
    try:
        con = sqlite3.connect("base.sqlite")
        cur = con.cursor()
        if login:
            cur.execute(f'SELECT * FROM profile WHERE login="{login}"')
        elif password:
            cur.execute(f'SELECT * FROM profile WHERE password="{password}"')
        elif id:
            cur.execute(f'SELECT * FROM profile WHERE id={id}')
        else:
            return None
        res = cur.fetchall()
    except:
        raise UnexpectedError('Непредвиденная ошибка')
    return res


def get_sessions_from_profile(id_):
    res = ''
    try:
        con = sqlite3.connect("base.sqlite")
        cur = con.cursor()

        cur.execute(f'''SELECT session_id, num_of_obj, time FROM sessions WHERE id_profile={id_}''')
        res = cur.fetchall()
    except Exception as E:
        print(E)
        raise UnexpectedError('Непредвиденная ошибка')
    return res


def change_login(login, new_login, password):
    if authorization(login, password):
        all_logins = [profile[1] for profile in get_all_profiles()]
        if new_login not in all_logins:
            try:
                con = sqlite3.connect("base.sqlite")
                cur = con.cursor()

                cur.execute(f'UPDATE profile SET login = ? WHERE login = ?', (new_login, login))
                con.commit()

                con.close()
            except:
                raise UnexpectedError('Непредвиденная ошибка')
        else:
            raise LoginAlreadyExists('Логин уже занят!')


def del_sessions_from_id(id_):
    con = sqlite3.connect("base.sqlite")
    cur = con.cursor()

    cur.execute(f'DELETE FROM sessions WHERE id_profile = {id_}')
    con.commit()

    con.close()


def del_sessions():  # WARNING!!!!!!
    con = sqlite3.connect("base.sqlite")
    cur = con.cursor()

    cur.execute('DELETE FROM sessions')
    con.commit()

    con.close()


def del_profiles():  # WARNING!!!!!!
    con = sqlite3.connect("profiles.db")
    cur = con.cursor()

    cur.execute('DELETE FROM profile')
    con.commit()

    con.close()
