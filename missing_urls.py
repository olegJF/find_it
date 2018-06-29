import psycopg2
import logging
import datetime
import requests

today = datetime.date.today()
from find_it.secret import DB_PASSWORD, DB_HOST, DB_NAME, DB_USER, MAILGUN_KEY, API, ADMIN_EMAIL

FROM_EMAIL = 'noreply@find_it.heroku.com'
SUBJECT = 'Недостающие урлы {}'.format(today)

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute(""" SELECT city_id, specialty_id FROM subscribers_subscriber WHERE is_active=%s;""", (True,))
    qs = cur.fetchall()
    cur.execute(""" SELECT * FROM scraping_city;""")
    cities_qs = cur.fetchall()
    cities = {i[0]: i[1] for i in cities_qs}
    cur.execute(""" SELECT * FROM scraping_specialty;""")
    sp_qs = cur.fetchall()
    sp = {i[0]: i[1] for i in sp_qs}
    mis_urls = []
    cnt = 'На дату {}  отсутствуют урлы для следующих пар:'.format(today)
    for pair in qs:
        cur.execute("""SELECT * FROM scraping_url  WHERE city_id=%s 
                    AND specialty_id=%s;""", (pair[0], pair[1]))
        qs = cur.fetchall()
        if not qs:
            mis_urls.append((cities[pair[0]], sp[pair[1]]))
    if mis_urls:
        for p in mis_urls:
            cnt += 'город -{}, специальность - {}'.format(p[0], p[1])
        
        requests.post(API,  auth=("api", MAILGUN_KEY), data={"from": FROM_EMAIL, "to": ADMIN_EMAIL,
                            "subject": SUBJECT, "text": cnt})

    conn.commit()
    cur.close()
    conn.close()