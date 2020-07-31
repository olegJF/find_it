from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from scraping.models import *
from scraping.forms import FindVacancyForm
import datetime


def index(request):
    form = FindVacancyForm
    return render(request, 'scraping/home.html', {'form': form})


# def vacancy_list(request):
#     form = FindVacancyForm
#     if request.GET:
#         try:
#             city_id = int(request.GET.get('city', None))
#             specialty_id = int(request.GET.get('specialty', None))
#         except (ValueError, TypeError):
#             raise Http404('Страница не найдена')
#         context = {}
#         context['form'] = form
#         if city_id and specialty_id:
#             qs = Vacancy.objects.filter(city=city_id, specialty=specialty_id)
#             paginator = Paginator(qs, 20)
#             page = request.GET.get('page')
#             try:
#                 qs = paginator.page(page)
#             except PageNotAnInteger:
#                 qs = paginator.page(1)
#             except EmptyPage:
#                 qs = paginator.page(paginator.num_pages)
#             if qs:
#                 context['jobs'] = qs
#                 context['city'] = qs[0].city.name
#                 context['specialty'] = qs[0].specialty.name
#                 context['city_id'] = qs[0].city.id
#                 context['specialty_id'] = qs[0].specialty.id
#             return render(request, 'scraping/list.html', context)
#         else:
#             raise Http404('Страница не найдена')
#
#     return render(request, 'scraping/list.html', {'form': form})


def list_view(request):
    # print(request.GET)
    form = FindVacancyForm()
    city = request.GET.get('city')
    specialty = request.GET.get('specialty')
    context = {'city': city, 'specialty': specialty, 'form': form}
    if city or specialty:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if specialty:
            _filter['specialty__slug'] = specialty

        qs = Vacancy.objects.filter(**_filter).select_related(
            'city', 'specialty')
        paginator = Paginator(qs, 20)
        page_number = request.GET.get('page')
        try:
            qs = paginator.page(page_number)
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)
        if qs:
            context['jobs'] = qs
            context['city_name'] = qs[0].city.name if city else ''
            context['sp_name'] = qs[0].specialty.name if specialty else ''
            # context['city_id'] = qs[0].city.id
            # context['specialty_id'] = qs[0].specialty.id
    return render(request, 'scraping/list.html', context)
