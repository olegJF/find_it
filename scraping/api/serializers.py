# -*- coding: utf-8 -*-

from scraping.models import City, Specialty, Vacancy
from rest_framework import serializers


class CitySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = City
        fields = ('name', 'slug')


class SpecialtySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Specialty
        fields = ('name', 'slug')
        

class VacancySerializer(serializers.ModelSerializer):
    city = CitySerializer()
    specialty = SpecialtySerializer()
    
    class Meta:
        model = Vacancy
        fields = ('city', 'specialty', 'timestamp', 'title', 'url', 
                    'description', 'company')
        
    