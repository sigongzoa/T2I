from django.urls import path
from . import views


urlpatterns = [
    path('copy', views.copy_db, name='copy'),
    path('rec', views.rec_page, name='rec'),
    path('db', views.save_db, name='db'),
    path('result', views.result_page, name='result'),
]