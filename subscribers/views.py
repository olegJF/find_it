from django.shortcuts import render, redirect, get_object_or_404
from .forms import (SubscriberModelForm, LogInForm, 
                    SubscriberHiddenEmailForm, ContactForm)
from django.views.generic.edit import FormView, CreateView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from .models import Subscriber
from find_it.secret import ADMIN_EMAIL, MAILGUN_KEY, API
import requests

class SubscriberCreate(CreateView):
    model = Subscriber
    form_class = SubscriberModelForm
    template_name = 'subscribers/create.html'
    success_url = reverse_lazy('create')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            messages.success(request, 'Данные успешно сохранены.')
            return self.form_valid(form)
        else:
            messages.error(request, 'Проверьте правильность заполнения формы')
            return self.form_invalid(form)

def login_subscriber(request):
    if request.method == "GET":
        form = LogInForm
        return render(request, 'subscribers/login.html', {'form': form})
    elif request.method == "POST":
        form = LogInForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            request.session['email'] = data['email']
            return redirect('update')
        return render(request, 'subscribers/login.html', {'form': form})
        

def update_subscriber(request):
    if request.method == 'GET' and request.session.get('email', False):
        email = request.session.get('email')
        qs = Subscriber.objects.filter(email=email).first()
        form = SubscriberHiddenEmailForm(initial={'email': qs.email, 'city': qs.city, 'specialty': qs.specialty, 
                                                    'password': qs.password, 'is_active': qs.is_active})
        return render(request, 'subscribers/update.html', {'form': form})
    elif request.method == 'POST':
        email = request.session.get('email')
        user = get_object_or_404(Subscriber, email=email)
        form = SubscriberHiddenEmailForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно сохранены.')
            del request.session['email']
            return redirect('list')
        messages.error(request, 'Проверьте правильность заполнения формы')
        return render(request, 'subscribers/update.html', {'form': form})
    else:
        return redirect('login')


def contact_admin(request):
    if request.method =='POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            city = form.cleaned_data['city']
            specialty = form.cleaned_data['specialty']
            from_email = form.cleaned_data['email']
            content = 'Прошу добавить в поиск , город {}'.format(city)
            content += ', специальность  {}'.format(specialty)
            content += 'Запрос от пользователя  {}'.format(from_email)
            Subject = 'Запрос на добавление в БД'
            requests.post(API,  auth=("api", MAILGUN_KEY), data={"from": from_email, "to": ADMIN_EMAIL,
                                "subject":Subject , "text": content})
            messages.success(request, 'Ваше письмо отправленно')
            return redirect('index')
        return render(request, 'subscribers/contact.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'subscribers/contact.html', {'form': form})