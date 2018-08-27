# -*- coding: utf-8 -*-
import datetime
from rest_framework import viewsets
from scraping.models import City, Specialty, Vacancy

from rest_framework.response import Response
from rest_framework.decorators import action
# from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .serializers import * 

TODAY = datetime.date.today()


class CityListAPIView(viewsets.ModelViewSet):
    
    queryset = City.objects.all()
    serializer_class = CitySerializer
    

class SpecialtyListAPIView(viewsets.ModelViewSet):
    
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
       

class VacancyListAPIView(viewsets.ModelViewSet):
    """ 
    
        ?city=kyiv&specialty=python
        
        city - slug for city filter;
        specialty - filter for specialty;
        
        
    """
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    
    def get_queryset(self):
        req = self.request
        city_slug = req.query_params.get('city')
        specialty_slug = req.query_params.get('specialty')
        qs = None
        
        if city_slug and specialty_slug:
            city, specialty = None, None
            city = City.objects.filter(slug=city_slug).first()
            if not city:
                city = City.objects.filter(slug=specialty_slug).first()
            specialty = Specialty.objects.filter(slug=specialty_slug).first()
            if not specialty:
                specialty = Specialty.objects.filter(slug=city_slug).first()
            period = TODAY - datetime.timedelta(1)
            if city and specialty:
                qs = Vacancy.objects.filter(city=city, specialty=specialty, 
                                timestamp__gte=period)
             
        self.queryset = qs    
        return self.queryset