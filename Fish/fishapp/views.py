from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *
menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']


def index(request):
    posts = Fish.objects.all()
    return render(request, 'fishapp/index.html',  {'posts': posts, 'menu': menu, 'title': 'Главная страница'})


def about(request):
    return render(request, 'fishapp/about.html', {'menu': menu,  'title': 'О сайте'})


def categories(request, categoryid):
    if (request.GET):
        print(request.GET)

    return HttpResponse(f'<h1>Статьи по категориям.</h1><p>{categoryid}</p>')


def archive(request, year):
    if int(year) > 2020:
        return redirect('home', permanent=True)
    return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')
