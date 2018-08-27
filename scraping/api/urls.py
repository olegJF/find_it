from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'cities', CityListAPIView)
router.register(r'specialties', SpecialtyListAPIView)
router.register(r'vacancies', VacancyListAPIView)

urlpatterns = []
urlpatterns += router.urls