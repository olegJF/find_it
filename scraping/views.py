from django.shortcuts import render
from scraping.models import *
from scraping.forms import FindVacancyForm
import datetime

def index(request):
    form = FindVacancyForm
    return render(request, 'scraping/home.html', {'form': form})


def vacancy_list(request):
    today = datetime.date.today()
    form = FindVacancyForm
    if request.GET:
        try:
            city_id = int(request.GET.get('city'))
            specialty_id = int(request.GET.get('specialty'))
        except ValueError:
            raise Http404('Страница не найдена')
        context = {}
        context['form'] = form
        qs = Vacancy.objects.filter(city=city_id, specialty=specialty_id)
        if qs:
            context['jobs'] = qs
            context['city'] = qs[0].city.name
            context['specialty'] = qs[0].specialty.name
            return render(request, 'scraping/list.html', context)

    return render(request, 'scraping/list.html', {'form': form})
