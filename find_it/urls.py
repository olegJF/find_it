"""find_it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from scraping.views import *
from subscribers.views import *

urlpatterns = [
    url(r'^adminka/', admin.site.urls),
    url(r'^list/', vacancy_list, name='list'),
    url(r'^login/', login_subscriber, name='login'),
    url(r'^update/', update_subscriber, name='update'),
    url(r'^create/', SubscriberCreate.as_view(), name='create'),
    url(r'^', index, name='index'),
]
