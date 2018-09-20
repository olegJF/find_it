from django.conf.urls import url, include
from django.contrib import admin
from scraping.views import *
from subscribers.views import *
import os

TOKEN = os.environ.get('BOT_TOKEN')

urlpatterns = [
    url(r'^adminka/', admin.site.urls),
    url(r'^api/{}/'.format(TOKEN ), include('scraping.api.urls')),
    url(r'^list/', vacancy_list, name='list'),
    url(r'^login/', login_subscriber, name='login'),
    url(r'^update/', update_subscriber, name='update'),
    url(r'^create/', SubscriberCreate.as_view(), name='create'),
    url(r'^contact/', contact_admin, name='contact'),
    url(r'^$', index, name='index'),
]
