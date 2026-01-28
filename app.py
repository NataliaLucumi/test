from datetime import datetime, timedelta
from unittest import result
import uuid
#import os
from pymongo import MongoClient
from flask import Flask, render_template, request
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,JWTManager, jwt_required,get_jwt
#from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#load_dotenv()
host='mongodb://localhost'
port=27017
db_name='movies_db'
user_collection= None
movies_collection=None

app.config['JWT_SECRET_KEY'] = 'super-secret'
#app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)

jwt=JWTManager(app)

def connect_db():
    try:
        client = MongoClient(host+":"+str(port)+"/")
        db = client[db_name]
        client.admin.command('ping')
        global user_collection
        user_collection = db.users 
        global movies_collection
        movies_collection = db.movies
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def check_if_admin_exists(username):
    global user_collection
    query= {"username": {"$eq": username}}
    return list(user_collection.find(query))

def create_user(usr):
    global user_collection
    result = user_collection.insert_one(usr)
    usr["_id"]=str(result.inserted_id)
    return usr

def create_admin_if_exist(usr):
    check_admin= check_if_admin_exists(usr["username"])
    if len(check_admin)>0:
        return check_admin
    else:
        return create_user(usr)
    

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
        if role == 'gerente' or role == 'administrador':
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
@jwt_required()
def get_all_movies(id):
    global movies_collection
    found = movies_collection.find_one({"_id": ObjectId(id)})
    found["_id"]=str(found["_id"])

    if request.method == "GET":
        if id is not None:
            return found, 200
        else:
            return {"error": "Película con id "+id+" no encontrada"}, 404
    else:
        if id is not None:
            movies_collection.delete_one({"_id": ObjectId(id)})
            return found, 200
        else:
            return {}, 204
def normialize_movie(item):
    item["_id"]=str(item["_id"])
    return item
#Obtener todas las películas (con filtros)
@app.route('/api/movies/')
@jwt_required()
def get_movies():
    ano= request.args.get("año",0)
    query={"año": {"$gte": ano}}
    global movies_collection
    result= list(movies_collection.find(query))
    results = list(map(lambda mov: normialize_movie(mov), result))
    return results,200

def insert_movie(movie):
    global movies_collection
    result = movies_collection.insert_one(movie)
    movie["_id"]=str(result.inserted_id)
    return movie

#Agregar una nueva película
@app.route('/api/movies/', methods=["POST"])
@manager_required
def add_movie():
    return insert_movie(request.json), 200
       

# Actualizar una película
@app.route('/api/movies/<string:id>', methods=["PATCH"])
@jwt_required()
def put_movies(id):
    body = request.json
    genero=body.get("genero")
    found=movies_collection.find_one({"_id": ObjectId(id)})
    query = {"$set":{}} 
    if found is not None:
        if genero != None:
            query["$set"]["genero"]= genero
            movies_collection.update_one({"_id": ObjectId(id)},query)
            found=movies_collection.find_one({"_id": ObjectId(id)})
            found["_id"]=str(found["_id"])
        return found, 200
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
    if len(check_if_admin_exists(username)) > 0:
        return {"Error": "Datos Invalidos",
                "Message": "El usuario ya existe"}, 400
    else:
        new_user = {
            "username": username,
            "password": generate_password_hash(password),
            "role": 'cliente',
            "created_at": datetime.now()
        }
        
        user_created= create_user(new_user)
        return {'user': username, '_id': user_created["_id"]}, 201

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
    if len(check_if_admin_exists(username)) == 0:
        return {"Error": "Datos Invalidos",
                "Message": "El usuario no existe"}, 400
    else:
        user = check_if_admin_exists(username)[0]
        current_password= user["password"]

        if  check_password_hash(current_password, body_password):
            token = create_access_token(identity=username,additional_claims={"user_id": user.get("user_id"),"role": user.get("role")})
            return {'Message': 'Usuario Autenticado',
                    'Token': token}, 200
        else:
            return {"Error": "Datos Invalidos",
                    "Message": "Datos Incorrectos"}, 401
    
if __name__ == '__main__':
    connect_db()
    admin_user= {
            "username": "admin",
            "password": generate_password_hash("123456"),
            "role": "administrador",
            "created_at": datetime.now()
        }
    print(f"Admin user created: {create_admin_if_exist(admin_user)}")

app.run(debug=True,
            port=8001,
            host='0.0.0.0')
    
