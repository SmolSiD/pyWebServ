__author__ = 'user'
__author__ = 'Denis'
import sqlite3
conn=sqlite3.connect('Myproject\webServ\Student.db')
conn.execute("CREATE TABLE VM09 (surname TEXT, numb INTEGER)")
conn.execute("CREATE TABLE Users (login TEXT, pass TEXT)")
#conn.execute("INSERT INTO VM09 VALUES ('Сироткин',20)")
cur=conn.cursor()
arr=[
    ("Аникеева",1),
    ("Волчик",2),
    ("Горчакова",3),
    ("Дорофеев",4),
    ("Дьячок",5),
    ("Ершова",6),
    ("Занегин",7),
    ("Кашин",8),
    ("Кончин",9),
    ("Коршунова",10),
    ("Кузнецова",11),
    ("Куля",12),
    ("Логвинов",13),
    ("Марголин",14),
    ("Мелкумов",15),
    ("Младов",16),
    ("Полячков",17),
    ("Рязанов",18),
    ("Симдянкин",19),
    ("Сироткин",20),
    ("Степанов",21),
    ("Cухотин", 22),
    ("Тараканов",23),
    ("Тарасов",24),
    ("Телков",25),
    ("Тимофеева",26),
    ("Шеин",27),
    ("Шульга",28)
    ]
cur.executemany("INSERT INTO VM09 VALUES (?,?)",arr)
cur.close()
conn.commit()
conn.close()