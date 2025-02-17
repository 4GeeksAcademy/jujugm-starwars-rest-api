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
from models import db, User, People, Planets, Favorites
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

## GET ALL
@app.route('/user', methods=['GET'])
def get_all_users():

    data = db.session.scalars(db.select(User)).all()
    result = list(map(lambda item: item.serialize(),data))
    print(result)

    if result == []:
        return jsonify({"msg":"user does not exists"}), 404

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "results": result
    }

    return jsonify(response_body), 200


@app.route('/user/<int:id>', methods=['POST'])
def create_user():
    try :
        # si en try sucede algun tipo de error lo colocamos en el except:

        request_body = request.json
        print(request_body)
        user = db.session.execute(db.select(User) .filter_by (email=request_body ["email"])). scalar_one()

                # user = db.session.execute(db.select(Table) .filter_by (atributo de busqueda =request_body ["at de busqueda "])). scalar_one()

        return jsonify({"msg": "cannot create, user already exist"}), 400

    except: 
        user = User(email=request_body["email"], password=request_body["password"], is_active= request_body["is_active"])
        # crea user
        db.session.add(user)
        # agregar user
        db.session.commit()
        # commit = grabado en piedra
    

    return jsonify({"msg": "created"}), 201


@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user():
    try :
        # solo quiero hacer una busqueda y mostrarlo
        
        user_query_delete = db.session.execute(db.select(User) .filter_by (id=id)).scalar_one()
        print(User)
        db.session.delete(User)
        db.session.commit()
                # user = db.session.execute(db.select(Table) .filter_by (atributo de busqueda =request_body ["at de busqueda "])). scalar_one()

        return jsonify({"msg": "deleted"}), 200
    except:
        return jsonify({"msg":"user exist"}), 404

    # except: 
    # #     user = User(email=request_body["email"], password=request_body["password"], is_active= request_body["is_active"])
    # #     # crea user
    # #     db.session.add(user)
    # #     # agregar user
    # #     db.session.commit()
    # #     # commit = grabado en piedra
    

    #     return jsonify({"msg": "created"}), 201


@app.route('/people', methods=['GET'])
def get_all_people():
    data = db.session.scalars(db.select(People)).all()
    result = list(map(lambda item: item.serialize(), data))
    print(result)
    return jsonify(result), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    data = db.session.scalars(db.select(Planets)).all()
    result = list(map(lambda item: item.serialize(), data))
    print(result)
    return jsonify(result), 200

## GET ONE 
@app.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    try:
        print(id)
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
    
        return jsonify({"result":user.serialize()}), 200
    except:
        return jsonify({"msg":"user do not exist"}), 404
    

@app.route('/people/<int:id>', methods=['GET'])
def get_one_people(id):
    try:
        print(id)
        people = db.session.execute(db.select(People).filter_by(id=id)).scalar_one()

        return jsonify({"result":people.serialize()}), 200
    except:
        return jsonify({"msg":"people do not exist"}), 404
    

@app.route('/people/<int:id>', methods=['POST'])
def create_people():
    try :
        # si en try sucede algun tipo de error lo colocamos en el except:

        request_body = request.json
        print(request_body)
        people = db.session.execute(db.select(People) .filter_by (name=request_body ["name"])). scalar_one()

                # user = db.session.execute(db.select(Table) .filter_by (atributo de busqueda =request_body ["at de busqueda "])). scalar_one()

        return jsonify({"msg": "cannot create, person already exist"}), 400

    except: 
        people = People(name=request_body["name"])
        # crea user
        db.session.add(people)
        # agregar user
        db.session.commit()
        # commit = grabado en piedra
    

    return jsonify({"msg": "created"}), 201

@app.route('/planets/<int:id>', methods=['POST'])
def create_planet():
    try :
        # si en try sucede algun tipo de error lo colocamos en el except:

        request_body = request.json
        print(request_body)
        planet = db.session.execute(db.select(Planets) .filter_by (name=request_body ["name"])). scalar_one()

                # user = db.session.execute(db.select(Table) .filter_by (atributo de busqueda =request_body ["at de busqueda "])). scalar_one()

        return jsonify({"msg": "cannot create, planet already exist"}), 400

    except: 
        planet = Planets(name=request_body["name"], climate=request_body["climate"], population=request_body["population"], terrain=request_body["terrain"])
        # crea user
        db.session.add(planet)
        # agregar user
        db.session.commit()
        # commit = grabado en piedra
    

    return jsonify({"msg": "planet created"}), 201

    
@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planet(id):
    try:
        print(id)
        planet = db.session.execute(db.select(Planets).filter_by(id=id)).scalar_one()

        return jsonify({"result":planet.serialize()}), 200
    except:
        return jsonify({"msg":"planet do not exist"}), 404

    

# Obtener los favoritos de un usuario específico
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    results = [fav.serialize() for fav in favorites]
    
    if not results:
        return jsonify({"msg": "No favorites found for this user"}), 404
    
    return jsonify(results), 200

# Agregar un favorito
@app.route('/user/<int:user_id>/favorite', methods=['POST'])
def add_favorite(user_id):
    body = request.get_json()
    people_id = body.get("people_id")
    planet_id = body.get("planet_id")

    if not people_id and not planet_id:
        return jsonify({"msg": "Must provide a people_id or planet_id"}), 400

    new_favorite = Favorites(user_id=user_id, people_id=people_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite added successfully"}), 201

# elimina favorito

@app.route('/user/<int:user_id>/favorite/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(user_id, favorite_id):
    favorite = Favorites.query.filter_by(id=favorite_id, user_id=user_id).first()

    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite deleted successfully"}), 200

# elimina algún people

@app.route('/people/<int:id>', methods=['DELETE'])
def delete_people():
    try :
        # solo quiero hacer una busqueda y mostrarlo
        
        people = db.session.execute(db.select(People) .filter_by (id=id)).scalar_one()
        print(people)
        db.session.delete(People)
        db.session.commit()
                # user = db.session.execute(db.select(Table) .filter_by (atributo de busqueda =request_body ["at de busqueda "])). scalar_one()

        return jsonify({"msg": "deleted"}), 200
    except:
        return jsonify({"msg":"person exists"}), 404
    
    # elimina algún people

@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet():
    try :
        # solo quiero hacer una busqueda y mostrarlo
        
        planet = db.session.execute(db.select(Planets) .filter_by (id=id)).scalar_one()
        print(planet)
        db.session.delete(Planets)
        db.session.commit()
                # user = db.session.execute(db.select(Table) .filter_by (atributo de busqueda =request_body ["at de busqueda "])). scalar_one()

        return jsonify({"msg": "deleted"}), 200
    except:
        return jsonify({"msg":"planet exists"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
