from django.urls import path, re_path

from .views import categories, index, archive

urlpatterns = [
    path('', index, name='home'),
    path('categories/<int:categoryid>/', categories),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),

]