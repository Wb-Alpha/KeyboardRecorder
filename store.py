#插入数据
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

database = sqlite3.connect('InputData', check_same_thread=False)
database.row_factory = dict_factory
con = database.cursor()


def insert(count, time):
    sql = "insert into keyStatistics (time, count) values (?, ?)"
    parameter = (time, count)
    con.execute(sql, parameter)
    database.commit()

def update(count, time):
    sql = "update keyStatistics set count=? where time=?"
    parameter = (count, time)
    con.execute(sql, parameter)
    database.commit()

#函数用于查询记录是否存在
def isExist(time):
    sql = "select count from keyStatistics where time=?"
    info = con.execute(sql, (time,))
    init_data = info.fetchone()
    return init_data


#如果是没有对应的数据库表则新建数据库表
def initTable():
    con.execute('''create table if not exists keyStatistics
                (time varchar(30) primary key,
                count int not null);
                ''')
    database.commit()


