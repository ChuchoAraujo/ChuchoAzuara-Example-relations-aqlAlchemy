"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#########################################################  USERS #############################################################################################

#------------------------------- GET USERS -------------------------------
@app.route('/users', methods=['GET'])
def get_all_users():

    users = User.query.all()
    serialized_users = [user.serialize() for user in users]

    return jsonify(serialized_users), 200

#------------------------------- GET USER/ID -------------------------------
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = User.query.get(user_id)
    serialized_user = user.serialize()

    return jsonify(serialized_user), 200

#------------------------------- POST USERS -------------------------------
@app.route('/users', methods=['POST'])
def create_user():
    body = request.get_json()
    new_user = User(email = body['email'], password = body['password'])
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "msg": "User created successfully", 
        "user": user.serialize()
    }

    return jsonify(response_body), 200

#------------------------------- DELETE USERS -------------------------------

@app.route('/users/<int:user_id>', methods= ['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    response_body = {
        "msg": "User deleted", 
        "user": user.serialize()
    }

    return jsonify(response_body)


#########################################################  PEOPLE #############################################################################################

#------------------------------- GET PEOPLE -------------------------------
@app.route('/people', methods=['GET'])
def get_all_people():

    people = People.query.all()
    serialized_people = [p.serialize() for p in people]

    return jsonify(serialized_people), 200


#------------------------------- GET USER/ID -------------------------------
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):

    people = People.query.get(people_id)
    serialized_people = people.serialize()

    return jsonify(serialized_people), 200

#------------------------------- POST PEOPLE -------------------------------
@app.route('/people', methods=['POST'])
def create_people():
    body = request.get_json()
    new_people = People(name = body['name'], description = body['description'])
    db.session.add(new_people)
    db.session.commit()

    response_body = {
        "msg": "People created successfully", 
        "people": new_people.serialize()
    }

    return jsonify(response_body), 200


#------------------------------- DELETE USERS -------------------------------

@app.route('/people/<int:people_id>', methods= ['DELETE'])
def delete_people(people_id):
    people = People.query.get(people_id)
    db.session.delete(people)
    db.session.commit()

    response_body = {
        "msg": "people deleted", 
        "people": people.serialize()
    }

    return jsonify(response_body)


#########################################################  PLANETS#############################################################################################

#------------------------------- GET PLANETS -------------------------------
@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planet.query.all()
    serialized_planets = [p.serialize() for p in planets]

    return jsonify(serialized_planets), 200


#------------------------------- GET PLANET/ID -------------------------------
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planet.query.get(planet_id)
    serialized_planet = planet.serialize()

    return jsonify(serialized_planet), 200

#------------------------------- POST PEOPLE -------------------------------
@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.get_json()
    new_planet = Planet(name = body['name'], climate = body['climate'], terrain = body['terrain'])
    db.session.add(new_planet)
    db.session.commit()

    response_body = {
        "msg": "Planet created successfully", 
        "people": new_planet.serialize()
    }

    return jsonify(response_body), 200


#------------------------------- DELETE USERS -------------------------------

@app.route('/people/<int:planet_id>', methods= ['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    db.session.delete(planet)
    db.session.commit()

    response_body = {
        "msg": "planet deleted", 
        "people": planet.serialize()
    }

    return jsonify(response_body)



#########################################################  FAVORITES #############################################################################################

#------------------------------- POST FAV PEOPLE -------------------------------

@app.route('/users/<int:user_id>/people', methods=['POST'])
def add_favorite_people(user_id):
    # Capturamos la informacion del request body y accedemos al people id
    body = request.get_json()
    people_id = body['people_id']
    
    user = User.query.get(user_id)
    people = People.query.get(people_id)

    new_favorite = Favorite(user=user, people=people)
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "msg": "Favorito agregado correctamente", 
        "favorite": new_favorite.serialize()
    }

    return jsonify(response_body), 200

#------------------------------- GET USER ID FAVORITE -------------------------------

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    favorites = user.favorites
    serialized_favorites = [f.serialize() for f in favorites]

    response_body = {
        "msg": f"Aqui tienes los favoritos de {user.email}",
        "favorites": serialized_favorites
    }

    return jsonify(response_body), 200
