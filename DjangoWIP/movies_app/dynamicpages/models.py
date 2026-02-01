from mongoengine import Document, StringField, IntField

class MoviesItem(Document):
    # ELIMINA la línea de _id. MongoEngine lo maneja solo.
    nombre = StringField(max_length=200)
    genero = StringField()
    duracion_min = IntField()
    director = StringField(max_length=100)
    clasificacion = StringField(max_length=200)
    año = IntField() # Asegúrate que en Compass sea 'año'

    meta = {
        'collection': 'movies', # Nombre exacto de tu colección
        'strict': False         # Esto evita el error 500 si hay campos extra
    }

    def __str__(self):
        return self.nombre