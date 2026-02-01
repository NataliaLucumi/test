# pylint: disable=no-member
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from dynamicpages.models import MoviesItem
from .serializers import MoviesItemSerializer

@api_view(['GET'])
def lista_movies(request):
    """
    API manual - Solo lista todos los movies
    GET /api/movies/ → Lista todos los movies en JSON
    """
    # Obtener todos los movies publicados
    movies = MoviesItem.objects.filter(nombre=True)
    
    # Convertir a JSON usando el serializer
    serializer = MoviesItemSerializer(movies, many=True)
    
    # Devolver respuesta JSON
    return Response({
        'count': len(movies),
        'results': serializer.data
    })

@api_view(['POST'])
def crear_movies(request):
    """
    API manual - Solo crear movies
    POST /api/movies/create/ → Crear nueva movie desde JSON
    """
    serializer = MoviesItemSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_movies(request, pk):
    """
    API completa para una movie específica
    GET /api/movies/1/ → Detalle en JSON
    PUT /api/movies/1/ → Actualizar movie
    DELETE /api/movies/1/ → Eliminar movie
    """
    # En MongoDB, pk puede ser el string del ObjectId
    movie = get_object_or_404(MoviesItem, pk=pk, publicado=True)
    
    if request.method == 'GET':
        serializer = MoviesItemSerializer(movie)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MoviesItemSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def estadisticas_catalogo(request):
    """
    Endpoint personalizado - Estadísticas del catálogo
    """
    from django.contrib.auth.models import User
    
    stats = {
        'total_items': MoviesItem.objects.count(),
        'published_items': MoviesItem.objects.filter(nombre=True).count(),
        'draft_items': MoviesItem.objects.filter(nombre=False).count(),
    }
    
    # Obtener la movie más reciente
    latest = MoviesItem.objects.filter(nombre=True).order_by('nombre').first()
    
    if latest:
        stats['latest_item'] = {
            'nombre': latest.nombre,
            'autor': latest.director
        }
    
    return Response(stats)