import psycopg2
import logging
import datetime
from scraping.utils import *

today = datetime.date.today()
ten_days_ago = datetime.date.today() - datetime.timedelta(10)
from find_it.secret import DB_PASSWORD, DB_HOST, DB_NAME, DB_USER, MAILGUN_KEY, API

FROM_EMAIL = 'noreply@find_it.heroku.com'
SUBJECT = 'Список вакансий за {}'.format(today)
template = '<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body>'
end = '</body></html>'

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute(""" SELECT city_id, specialty_id FROM subscribers_subscriber WHERE is_active=%s;""", (True,))
    cities_qs = cur.fetchall()
    for pair in cities_qs:
        content = ''
        city = pair[0]
        specialty = pair[1]
        cur.execute(""" SELECT email FROM subscribers_subscriber WHERE is_active=%s 
                            AND city_id=%s AND specialty_id=%s;""", (True, city, specialty))
        email_qs = cur.fetchall()
        emails = [i[0] for i in email_qs]
        cur.execute("""SELECT url, title, description, company FROM scraping_vacancy WHERE city_id=%s 
                        AND specialty_id=%s AND timestamp=%s; """, (city, specialty, today ))
        jobs_qs = cur.fetchall()
        if jobs_qs:
            for job in jobs_qs:
                content += '<a href="{}" target="_blank">'.format(job[0])
                content += '{}</a><br/>'.format(job[1])
                content += '<p>{}</p>'.format(job[2])
                content += '<p>{}</p><br/>'.format(job[3])
                content += '<hr/><br/><br/>'
            html_m = template + content + end
            for email in emails:
                requests.post(API,  auth=("api", MAILGUN_KEY), data={"from": FROM_EMAIL, "to": email,
                                "subject": SUBJECT, "html": html_m})
        else:
            requests.post(API,  auth=("api", MAILGUN_KEY), data={"from": FROM_EMAIL, "to": email,
                                "subject": SUBJECT, "text": 'Список вакансий по Вашему профилю на сегодня пуст.'})
    conn.commit()
    cur.close()
    conn.close()