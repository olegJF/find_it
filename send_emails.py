import psycopg2
import logging
import datetime
import os
import requests
import smtplib
import time


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

today = datetime.date.today()
ten_days_ago = datetime.date.today() - datetime.timedelta(10)

dir = os.path.dirname(os.path.abspath('db.py'))
path = ''.join([dir, '\\find_it\\secret.py'])
if os.path.exists(path):
    from find_it.secret import (DB_PASSWORD, DB_HOST, DB_NAME, DB_USER, 
                                MAILGUN_KEY, API, MAIL_SERVER, 
                                PASSWORD_AWARD, USER_AWARD, FROM_EMAIL)
else:
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    MAILGUN_KEY = os.environ.get('MAILGUN_KEY')
    API = os.environ.get('API')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    PASSWORD_AWARD = os.environ.get('PASSWORD_AWARD')
    USER_AWARD = os.environ.get('USER_AWARD')
    FROM_EMAIL = os.environ.get('FROM_EMAIL')

FROM_ = 'Вакансии <{email}>'.format(email=FROM_EMAIL)
SUBJECT = 'Список вакансий за  {}'.format(today)
template = '''<!doctype html><html lang="en">
                <head><meta charset="utf-8"></head>
                <body>'''
end = '</body></html>'


try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, 
                            host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute(""" SELECT city_id, specialty_id FROM subscribers_subscriber 
                    WHERE is_active=%s;""", (True,))
    cities_qs = cur.fetchall()
    
    for pair in cities_qs:
        content = '''<h3>Список вакансий, согласно Ваших предпочтений. </h3>
                    <hr><br/><br/>'''
        city = pair[0]
        specialty = pair[1]
        cur.execute(""" SELECT email FROM subscribers_subscriber 
                            WHERE is_active=%s 
                            AND city_id=%s AND specialty_id=%s;""", 
                            (True, city, specialty))
        email_qs = cur.fetchall()
        emails = [i[0] for i in email_qs]
        cur.execute("""SELECT url, title, description, company 
                        FROM scraping_vacancy WHERE city_id=%s 
                        AND specialty_id=%s AND timestamp=%s; """, 
                        (city, specialty, today ))
        jobs_qs = cur.fetchall()
        
        if jobs_qs:
            for job in jobs_qs:
                content += '<a href="{}" target="_blank">'.format(job[0])
                content += '{}</a><br/>'.format(job[1])
                content += '<p>{}</p>'.format(job[2])
                content += '<p>{}</p><br/>'.format(job[3])
                content += '<hr/><br/><br/>'
            content += '''<h4>Вы получили данное письмо потому, что подписались 
                            на <a href="{}" target="_blank">
                            сервис по рассылке вакансий </a> согласно вашиx 
                            предпочтений<h4><br/>
                            <h5>Спасибо, что Вы с нами! </h5><br/>
                            '''.format('jobfinderapp.herokuapp.com')
            html_m = template + content + end
            for email in emails:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = SUBJECT
                msg['From'] = FROM_
                msg['To'] = email
                mail = smtplib.SMTP()
                mail.connect(MAIL_SERVER, 25)
                mail.ehlo()
                mail.starttls()
                mail.login(USER_AWARD, PASSWORD_AWARD)
                part = MIMEText(html_m, 'html')
                msg.attach(part)
                mail.sendmail(FROM_EMAIL, [email], msg.as_string())
                time.sleep(5)
                mail.quit()
        # else:
        #     content = '''<h3>На сегодня, список вакансий по 
        #                         Вашему запросу, пуст.</h3> '''
        #     html_m = template + content + end
        #     part = MIMEText(html_m, 'html')
        #     msg.attach(part)
        #     mail.sendmail(FROM_EMAIL, emails, msg.as_string())
            # for email in emails:
            #     msg['To'] = email
            #     mail.sendmail(FROM_EMAIL, email, msg.as_string())
            #     time.sleep(2)
        
    conn.commit()
    cur.close()
    conn.close()
    