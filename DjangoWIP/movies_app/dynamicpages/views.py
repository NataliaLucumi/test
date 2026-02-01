# pylint: disable=no-member
from django.shortcuts import render
from .models import MoviesItem

def lista_movies(request):
    """Vista que consulta MongoDB y pasa datos al template"""
    # MongoEngine usa la misma sintaxis de consulta que Django ORM
    movies = MoviesItem.objects.filter(nombre=True).order_by('nombre')
    
    # El contexto son los datos que se pasan al template
    contexto = {
        'movies': movies,
        'titulo_pagina': 'Catálogo de Películas'
    }
    
    # render() combina el template con el contexto
    return render(request, 'dynamicpages/lista_movies.html', contexto)

def detalle_movies(request, movies_id):
    """Vista que muestra un movies específico desde MongoDB"""
    # En MongoDB el ID es un ObjectId, pero podemos usar el string
    movies = MoviesItem.objects.get(id=movies_id, nombre=True)
    
    contexto = {
        'movies': movies
    }
    
    return render(request, 'dynamicpages/detalle_movies.html', contexto)