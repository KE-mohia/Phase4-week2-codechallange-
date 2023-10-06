from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from models import db, Hero, Power, HeroPower
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Error handler for 404 - Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404

# Error handler for 400 - Bad Request (for validation errors)
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "errors": error.description}), 400

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
    return jsonify(hero_data)

# GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero is None:
        abort(404)
    
    powers = [{"id": hp.power.id, "name": hp.power.name, "description": hp.power.description} for hp in hero.powers]

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": powers
    }
    return jsonify(hero_data)

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(power_data)

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power is None:
        abort(404)
    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }
    return jsonify(power_data)

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        abort(404)
    try:
        data = request.get_json()
        if 'description' in data:
            new_description = data['description']
            if len(new_description) >= 20:
                power.description = new_description
                db.session.commit()
                return jsonify({"id": power.id, "name": power.name, "description": power.description})
            else:
                raise ValueError("Description must be at least 20 characters long.")
        else:
            raise ValueError("No 'description' provided in the request.")
    except ValueError as e:
        abort(400, description=str(e))
        
# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        if not strength or not power_id or not hero_id:
            raise ValueError("Required fields missing in the request.")

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if hero is None or power is None:
            abort(404)

        hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id,
                               created_at=datetime.now(), updated_at=datetime.now())

        db.session.add(hero_power)
        db.session.commit()

        # Fetch updated hero data with powers
        powers = [{"id": hero_power.power.id, "name": hero_power.power.name, "description": hero_power.power.description}]
        
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": powers
        }

        return jsonify(hero_data), 201
    except ValueError as e:
        abort(400, description=str(e))

if __name__ == '__main__':
    app.run(port=5555)
