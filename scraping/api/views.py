# -*- coding: utf-8 -*-
import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
    permission_classes = (IsAuthenticatedOrReadOnly,)
    

class SpecialtyListAPIView(viewsets.ModelViewSet):
    
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
       

class VacancyListAPIView(viewsets.ModelViewSet):
    """ 
    
        ?city=kyiv&sp=python
        
        city - slug for city filter;
        specialty - filter for specialty;
        
        
    """
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    def get_queryset(self):
        req = self.request
        city_slug = req.query_params.get('city')
        specialty_slug = req.query_params.get('sp')
        qs = None
        period = TODAY - datetime.timedelta(1)
        if city_slug and specialty_slug:
            qs = Vacancy.objects.filter(city__slug=city_slug, 
                                        specialty__slug=specialty_slug, 
                                        timestamp__gte=period)
            if not qs.exists():
                qs = Vacancy.objects.filter(city__slug=specialty_slug, 
                                        specialty__slug=city_slug, 
                                        timestamp__gte=period)
             
        self.queryset = qs    
        return self.queryset
