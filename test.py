# database
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

database = sqlite3.connect('InputData')
database.row_factory = dict_factory
con = database.cursor()
#con.execute("insert into keyStatistics values (?, 555)", ("1989-06-05",))
#database.commit()
lasts = con.execute("select * from keyStatistics where time=?", ("2020-05-28", ))
times=lasts.fetchall()
print(times)
#print(lasts.fetchone()["count"])

