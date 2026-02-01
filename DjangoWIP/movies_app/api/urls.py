from django.urls import path
from . import views

urlpatterns = [
    # URLs explícitas - cada acción tiene su propio endpoint
    path('', views.lista_movies, name='api_lista_movies'),
    path('create/', views.crear_movies, name='api_crear_movies'),
    path('<str:pk>/', views.detalle_movies, name='api_detalle_movies'),
    path('stats/', views.estadisticas_catalogo, name='api_estadisticas'),
]