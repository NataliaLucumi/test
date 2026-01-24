from datetime import datetime, timedelta
import uuid
import os
from flask import Flask, request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,JWTManager, jwt_required,get_jwt


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'
#app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)

jwt=JWTManager(app)

def get_token_role():
    try:
        claims = get_jwt()
        return claims.get('role','user')
    except:
            return None

#Definir Roles  
def manager_required(f):
    @jwt_required()
    def custom_validation(*args, **kwargs):
        role=get_token_role()
        if role == 'gerente':
            return f(*args, **kwargs)
        else:
            print(f"Debug Role: {role}")
            return {
                "Error": "Permisos insuficientes", 
                "Message": "El usuario no tiene permisos de Gerente"
            }, 403  
    return custom_validation

def admin_required(f):
    @jwt_required()
    def custom_validation_admin(*args, **kwargs):
        role=get_token_role()
        if role == 'administrador':
            return f(*args, **kwargs)
        else:
            print(f"Debug Role: {role}")
            return {
                "Error": "Permisos insuficientes", 
                "Message": "El usuario no tiene permisos de Administrador"
            }, 403  
    return custom_validation_admin

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

#Tarea aplicación Flask con tu tema favorito PELICULAS
movies = {
    "1": {
        "nombre": "Rapidos y Furiosos",
        "genero": "Acción",
        "año": 2010,
        "director": "Justin Lin",
        "duracion_min": 107,
        "clasificacion": "Mayores de 13 años"
    },
    "2": {
        "nombre": "Zootopia",
        "genero": "Aventura",
        "año": 2016,
        "director": "Byron Howard",
        "duracion_min": 108,
        "clasificacion": "Todos los públicos"
    },
    "3": {
        "nombre": "El Paseo 7",
        "genero": "Comedia",
        "año": 2023,
        "director": "Harold Trompetero",
        "duracion_min": 90,
        "clasificacion": "Mayores de 18 años"
    },
    "4": {
        "nombre": "Avengers",
        "genero": "Acción",
        "año": 2020,
        "director": "Joss Whedon",
        "duracion_min": 143,
        "clasificacion": "Mayores de 13 años"
    },
    "5": {
        "nombre": "La Oscuridad",
        "genero": "Terror",
        "año": 2021,
        "director": "Desconocido",
        "duracion_min": 95,
        "clasificacion": "Mayores de 18 años"
    }
}

# Consultar o eliminar una película por id
@app.route('/api/movies/<string:id>', methods=["GET", "DELETE"])
def get_all_movies(id):
    print(f"Method: {request.method}")
    if request.method == "GET":
        if id in movies:
            return movies[id], 200
        else:
            return {"error": "Película con id "+id+" no encontrada"}, 404
    else:
        if id in movies:
            element = movies[id]
            del movies[id]
            return element, 200
        else:
            return {}, 204

#Obtener todas las películas (con filtros)
@app.route('/api/movies/')
@jwt_required()
def get_movies():
    ano= request.args.get("año",0)
    filtered = list(filter(lambda key: movies[key]["año"] >= int(ano), movies))
    return list(map(lambda k: movies[k], filtered))

#Agregar una nueva película
@app.route('/api/movies/', methods=["POST"])
@manager_required
def add_movie():
    body = request.json
    copy = body.copy()
    new_id =body["id"]
    if new_id in movies:
        return {"Message": "La película con id "+new_id+" ya existe"}, 409    
    else:
        del body["id"]
        movies[new_id] = body
        return copy, 201

# Actualizar una película
@app.route('/api/movies/<string:id>', methods=["PATCH"])
@jwt_required()
def put_movies(id):
    body = request.json
    genero=body.get("genero")
    if id in movies:
        if genero != None:
            movies[id]["genero"]=genero
        return movies[id], 200
    else:
        return {"error": "Película con id "+id+" no encontrada"}, 404
    
#Autenticación básica
users = [
            {
            "id": "admin-1",
            "username": "admin",
            "password": generate_password_hash("123456"),
            "role": "administrador",
            "created_at": datetime.now()
        }
        ]

def get_users_by_username(username):
    return list(filter(lambda u: u['username'] == username, users)) 

#Sign Administrador
@app.route('/api/admin/signIn', methods=["POST"])
@admin_required
def sign_in_admin():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return {"Error": "Datos Invalidos",
                "Message": "Se requieren Username y Password"}, 400
    else:
        username = request.json["username"]
        password = request.json["password"]
        #role = request.json["role"]
    if len(get_users_by_username(username)) > 0:
        return {"Error": "Datos Invalidos",
                "Message": "El usuario ya existe"}, 400
    else:
        user_id = 'user-' + str(uuid.uuid4())
        new_user = {
            "id": user_id,
            "username": username,
            "password": generate_password_hash(password),
            "role": "gerente",
            "created_at": datetime.now()
        }
        users.append(new_user)
        return {'user': username}, 201
    
#Sign In Publico
@app.route('/api/singIn', methods=["POST"])
def sign_in():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return {"Error": "Datos Invalidos",
                "Message": "Se requieren Username y Password"}, 400
    else:
        username = request.json["username"]
        password = request.json["password"]
        #role = request.json["role"]
    if len(get_users_by_username(username)) > 0:
        return {"Error": "Datos Invalidos",
                "Message": "El usuario ya existe"}, 400
    else:
        user_id = 'user-' + str(uuid.uuid4())
        new_user = {
            "id": user_id,
            "username": username,
            "password": generate_password_hash(password),
            "role": "cliente",
            "created_at": datetime.now()
        }
        users.append(new_user)
        return {'user': username}, 201

@app.route('/api/user/<string:username>', methods=["GET"])
def get_user(username):
    return get_users_by_username(username)[0], 200
    
@app.route('/api/login', methods=["POST"])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return {"Error": "Datos Invalidos",
                "Message": "Se requieren Username y Password"}, 400
    else:
        username = request.json["username"]
        body_password = request.json["password"]
    if len(get_users_by_username(username)) == 0:
        return {"Error": "Datos Invalidos",
                "Message": "El usuario no existe"}, 400
    else:
        user = get_users_by_username(username)[0]
        current_password= user["password"]

        if  check_password_hash(current_password, body_password):
            token = create_access_token(identity=username,additional_claims={"user_id": user.get("user_id"),"role": user.get("role")})
            return {'Message': 'Usuario Autenticado',
                    'Token': token}, 200
        else:
            return {"Error": "Datos Invalidos",
                    "Message": "Datos Incorrectos"}, 401
    
if __name__ == '__main__':
    app.run(debug=True,
            port=8001,
            host='0.0.0.0')