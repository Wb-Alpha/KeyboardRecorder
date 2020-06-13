# 插入数据
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


database = sqlite3.connect('InputData', check_same_thread=False)
database.row_factory = dict_factory
con = database.cursor()


def insert(time, kb_count, ms_count):
    sql = "insert into keyStatistics (time, kb_count, ms_count) values (?, ?, ?)"
    parameter = (time, kb_count, ms_count)
    con.execute(sql, parameter)
    database.commit()


def update(time, kb_count, ms_count):
    sql = "update keyStatistics set kb_count=?, ms_count=? where time=?"
    parameter = (kb_count, ms_count, time)
    con.execute(sql, parameter)
    database.commit()


# 函数用于查询记录是否存在
def isExist(time):
    sql = "select kb_count, ms_count from keyStatistics where time=?"
    info = con.execute(sql, (time,))
    init_data = info.fetchone()
    print(init_data)
    return init_data


# 如果是没有对应的数据库表则新建数据库表
def initTable():
    con.execute('''create table if not exists keyStatistics
                (time varchar(30) primary key,
                kb_count int not null,
                ms_count int not null);
                ''')
    database.commit()
