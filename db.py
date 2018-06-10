import psycopg2
import logging
import datetime

today = datetime.date.today()
from find_it.secret import DB_PASSWORD, DB_HOST, DB_NAME, DB_USER

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute(""" SELECT city_id, specialty_id FROM subscribers_subscriber WHERE is_active=%s;""", (True,))
    cities_qs = cur.fetchall()
    print(cities_qs)
    todo_list = {i[0]:set() for i in cities_qs}
    for i in cities_qs:
        todo_list[i[0]].add(i[1])
    print(todo_list)
    conn.commit()
    cur.close()
    conn.close()