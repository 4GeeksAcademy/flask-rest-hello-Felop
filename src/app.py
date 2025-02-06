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
from models import db, User,Character, Planet, Favorite
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

@app.route('/users', methods=['GET'])
def get_users():
    users=User.query.all()
    users_list=[user.serialize()for user in users]
    return jsonify(users_list),200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id=1
    user=User.query.get(user_id)
    if not user:
        return jsonify({"error":"user not found"}),404
    favorites=[fav.serialize()for fav in user.favorite]
    return jsonify(favorites),200

@app.route('/people', methods=['GET'])
def get_all_characters():
    characters=Character.query.all()
    characters_list=[char.serialize()for char in characters]
    return jsonify(characters_list),200

@app.route('/people/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character=Character.query.get(character_id)
    if not character:
        return jsonify({"error":"Character no found"}),404
    return jsonify(character.serialize()),200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets=Planet.query.all()
    planets_list=[planet.serialize()for planet in planets]
    return jsonify(planets_list),200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet=Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error":"Planet not found"}),404
    return jsonify(planet.serialize()),200

@app.route('/favorite/<string:type>/<int:item_id>', methods=['POST'])
def add_favorite(type, item_id):
    user_id=1

    if type == "people":
        item=Character.query.get(item_id)
        if not item:
            return jsonify({"error":"Character not found"}),404
        new_fav= Favorite(user_id=user_id,character_id=item_id)

    elif type == "planet":
        item= Planet.query.get(item_id) 
        if not item:
            return jsonify({"error":"Planet not found"}),404
        new_fav= Favorite(user_id=user_id, planet_id=item_id)

    else:
        return jsonify({"error":"Invalid favorite type"}),400

    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"message": f"{type.capitalize()} added to favorites"}), 201    


@app.route('/favorite/<string:type>/<int:item_id>', methods=['DELETE'])
def delete_favorite(type,item_id):
    user_id=1

    if type == "people":
        favorite= Favorite.filter_by(user_id=user_id,character_id=item_id).first()
    elif type=="planet":
        favorite=Favorite.filter_by(user_id=user_id,planet_id=item_id).first()   
    else:
        return jsonify({"error":"Invalid favorite type"}),400
    if not favorite:
        return jsonify({"error":"Favorite not found"}),404   
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": f"{type.capitalize()} removed from favorites"}), 200 




   
    

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
