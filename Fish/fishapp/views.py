from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *


def index(request):
    posts = Fish.objects.all()
    context = {
        'posts': posts,
        'title': 'Главная страница',
        'cat_selected': 0
    }
    return render(request, 'fishapp/index.html', context=context)


def about(request):
    return render(request, 'fishapp/about.html', {'title': 'О сайте'})


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            try:
                Fish.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, "Ошибка добавления поста")
    else:
        form = AddPostForm()
    return render(request, 'fishapp/addpage.html', {'form': form, 'title': 'Добавление статьи'})


def login(request):
    return HttpResponse('Аторитизация')


def contact(request):
    return HttpResponse('Обратная связь')


def show_post(request, post_slug):
    post = get_object_or_404(Fish, slug=post_slug)

    context = {
        'post': post,
        "title": post.title,
        'cat_selected': post.cat_id,
    }
    return render(request, 'fishapp/post.html', context=context)


def show_category(request, cat_slug):
    posts = Fish.objects.filter(cat__slug=cat_slug)
    if len(posts) == 0:
        raise Http404
    context = {
        'posts': posts,
        'title': 'Отображение по рубрикам',
        'cat_selected': posts[0].cat_id
    }
    return render(request, 'fishapp/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')
