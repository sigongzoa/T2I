from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('rec', views.rec_page, name='rec'),
    path('test', views.test, name='test'),
]