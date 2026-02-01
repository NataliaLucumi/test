# dynamicpages/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_movies, name='lista_movies'),
    path('movies/<str:movies_id>/', views.detalle_movies, name='detalle_movies'),
]