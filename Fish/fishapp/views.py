from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView, CreateView
from .forms import *
from .models import *


class FishHome(ListView):
    model = Fish
    template_name = 'fishapp/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Fish.objects.filter(is_published=True)


'''    
def index(request):
    posts = Fish.objects.all()
    context = {
        'posts': posts,
        'title': 'Главная страница',
        'cat_selected': 0
    }
    return render(request, 'fishapp/index.html', context=context)
'''


def about(request):
    return render(request, 'fishapp/about.html', {'title': 'О сайте'})


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'fishapp/addpage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        return context


'''
def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'fishapp/addpage.html', {'form': form, 'title': 'Добавление статьи'})
'''


def login(request):
    return HttpResponse('Аторитизация')


def contact(request):
    return HttpResponse('Обратная связь')


class ShowPost(DeleteView):
    model = Fish
    template_name = 'fishapp/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        return context


'''
def show_post(request, post_slug):
    post = get_object_or_404(Fish, slug=post_slug)

    context = {
        'post': post,
        "title": post.title,
        'cat_selected': post.cat_id,
    }
    return render(request, 'fishapp/post.html', context=context)
'''


class FishCategory(ListView):
    model = Fish
    template_name = 'fishapp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Fish.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id
        return context


"""
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
"""


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')
