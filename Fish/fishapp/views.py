from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView
from .forms import *
from .models import *
from .utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


class FishHome(DataMixin, ListView):
    paginate_by = 3
    model = Fish
    template_name = 'fishapp/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

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
    contact_list = Fish.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'fishapp/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'fishapp/addpage.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


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


class ShowPost(DataMixin, DeleteView):
    model = Fish
    template_name = 'fishapp/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


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


class FishCategory(DataMixin, ListView):
    model = Fish
    template_name = 'fishapp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Fish.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Категория - " + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)

        return dict(list(context.items()) + list(c_def.items()))


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
