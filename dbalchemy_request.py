from dbalchemy import *
from time import sleep
import telebot
import sqlite3





def record_user(FCs):
    with engine.connect() as conn:
        stmt = insert(Users).values(
            name = FCs[0],
            sur_name = FCs[1],
            father_name = FCs[2],
            telephone = FCs[3],
            email = FCs[4]
        )
        conn.execute(stmt)
        conn.commit()


def add_user_telephone(id_and_telephone):
    with engine.connect() as conn:
        stmt1 = update(Users).where(Users.id == id_and_telephone[0]).values(telephone=id_and_telephone[1])
        conn.execute(stmt1)
        conn.commit()


def add_user_email(id_and_email):
    with engine.connect() as conn:
        stmt2 = update(Users).where(Users.id == id_and_email[0]).values(email=id_and_email[1])
        conn.execute(stmt2)
        conn.commit()



def view():
    with engine.connect() as conn:
        row = conn.execute(select(Users)).all()
        table = inspect(Users)
        info = []
        columns = []
        user = '-'*35 + '\n'
        for column in table.c:
             columns.append(column.name)
        for i in row:
            for j in range(len(i)):
                user = user + str(columns[j]) + ' : ' + str(i[j]) + '\n'
            user = user + '-'*40 + '\n'
            info.append(user)
            user =''
    return "".join(info)


def delete(id_users):
    conn = sqlite3.connect('dataspace.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Users WHERE id = (?);', (id_users,))
    conn.commit()
    cursor.close()











# conn = sqlite3.connect('dataspace.db')
# cursor = conn.cursor()
# cursor.execute('DROP TABLE Prepods;')
# conn.commit()
# cursor.close()

