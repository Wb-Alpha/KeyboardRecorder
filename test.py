import sqlite3
import datetime

from pynput import mouse

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# 如果是没有对应的数据库表则新建数据库表
def initTable():
    con.execute('''create table keyStatistics
                (time varchar(30) primary key,
                kb_count int not null,
                ms_count int not null);
                ''')
    database.commit()


database = sqlite3.connect('InputData', check_same_thread=False)
database.row_factory = dict_factory
con = database.cursor()
print(datetime.datetime.now().date())
con.execute("insert into keyStatistics (time, kb_count, ms_count) values (?, 423, 5235)", (datetime.datetime.now().date(), ))
database.commit()
