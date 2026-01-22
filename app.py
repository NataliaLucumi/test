from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/hello/<string:name>')
def grettings(name):
    return "<h1>Hello! "+name+"</h1>"

saludo ={"ES": "Hola Mundo!",
         "EN": "Hello World!",} 

@app.route('/dynamic-hello/<string:name>/')
def data(name):
    language = request.args.get("language","EN")
    uppercase = request.args.get("uppercase",False)
    phase= saludo[language] + " " + name
    if uppercase == "true" or uppercase == "True":
        phase = phase.upper()
    return "<h1>"+phase+"</h1>"

pets = { "Firulais": {"raza": "Hamster", "edad": 5},
    "Coco": {"raza": "Gato", "edad": 3},
    "Mila": {"raza": "Perro", "edad": 2 }}

@app.route('/pet/<string:name>')
def get_pets(name):
    if name in pets:
        return pets[name]
    else:
        return {"error": "No se encontró la mascota"}, 404
    
#Tarea aplicación Flask con tu tema favorito PELICULAS
movies = {
    "Rapidos y Furiosos": {
        "genero": "Acción",
        "año": 2010,
        "director": "Justin Lin",
        "duracion_min": 107,
        "clasificacion": "Mayores de 13 años"
    },
    "Zootopia": {
        "genero": "Aventura",
        "año": 2016,
        "director": "Byron Howard",
        "duracion_min": 108,
        "clasificacion": "Todos los públicos"
    },
    "El Paseo 7": {
        "genero": "Comedia",
        "año": 2023,
        "director": "Harold Trompetero",
        "duracion_min": 90,
        "clasificacion": "Mayores de 18 años"
    },
    "Avengers": {
        "genero": "Acción",
        "año": 2020,
        "director": "Joss Whedon",
        "duracion_min": 143,
        "clasificacion": "Mayores de 13 años"
    },
    "La Oscuridad": {
        "genero": "Terror",
        "año": 2021,
        "director": "Desconocido",
        "duracion_min": 95,
        "clasificacion": "Mayores de 18 años"
    }
}

#Obtener todas las películas (con filtros)
@app.route("/movies", methods=["GET"])
def get_movies():
    genero = request.args.get("genero")
    año = request.args.get("año")

    resultado = movies

    if genero:
        resultado = {
            k: v for k, v in resultado.items()
            if v["genero"].lower() == genero.lower()
        }

    if año:
        resultado = {
            k: v for k, v in resultado.items()
            if str(v["año"]) == año
        }

    return jsonify(resultado)

# Obtener TODAS las películas
@app.route("/movies", methods=["GET"])
def get_all_movies():
    return jsonify(movies)

#Obtener un tema
@app.route("/movies/<string:nombre>", methods=["GET"])
def get_movie(nombre):
    movie = movies.get(nombre)
    if movie:
        return jsonify(movie)
    return jsonify({"error": "Película no encontrada"}), 404

#Agregar una nueva película
@app.route("/movies", methods=["POST"])
def add_movie():
    data = request.json
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    movies[nombre] = {
        "genero": data.get("genero"),
        "año": data.get("año"),
        "director": data.get("director"),
        "duracion_min": data.get("duracion_min"),
        "clasificacion": data.get("clasificacion")
    }

    return jsonify({"mensaje": "Película agregada"}), 201

#Eliminar una película
@app.route("/movies/<string:nombre>", methods=["DELETE"])
def delete_movie(nombre):
    if nombre in movies:
        del movies[nombre]
        return jsonify({"mensaje": "Película eliminada"}), 200
    return jsonify({"error": "Película no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True,
            port=8001,
            host='0.0.0.0')