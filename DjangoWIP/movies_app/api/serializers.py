# pylint: disable=no-member
from rest_framework import serializers
from dynamicpages.models import  MoviesItem

class MoviesItemSerializer(serializers.Serializer):
    """Convierte MoviesItem (MongoDB) ↔ JSON"""
    _id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(max_length=200)
    genero = serializers.CharField()
    duracion_min = serializers.IntegerField()
    director = serializers.CharField(max_length=100)
    clasificacion = serializers.CharField(max_length=200)
    año = serializers.IntegerField()
    
    def create(self, validated_data):
        """Crear nuevo movies en MongoDB"""
        return MoviesItem(**validated_data).save()
    
    def update(self, instance, validated_data):
        """Actualizar movies existente en MongoDB"""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance