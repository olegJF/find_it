from django.shortcuts import render
from scraping.utils import *
from scraping.models import *


def home(request):
    jobs = djinni()
    city = City.objects.get(name='Киев')
    specialty = Specialty.objects.get(name='Python')
    v = Vacancy.objects.filter(city=city.id, specialty=specialty.id).values('url')
    url_list = [i['url'] for i in v]
    for job in jobs:
        if job['href'] not in url_list:
            vacancy = Vacancy(city=city, specialty=specialty, url=job['href'],
                                title=job['title'], description=job['descript'], company=job['company'])
            vacancy.save()

    return render(request, 'base.html', {'jobs': jobs})