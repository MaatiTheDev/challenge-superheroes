from flask import Flask, request
from flask_migrate import Migrate
from models import db, Hero, HeroPower, Power

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)
Migrate(app, db)


@app.route('/')
def get_index():
    """Return a string indicating that the API is live."""

    return 'Superheroes API'


@app.route('/heroes', methods=['GET'])
def get_heroes():
    """Get a list of all the heroes."""

    heroes = Hero.query.all()

    return [hero.to_dict(rules=('-hero_power_list', )) for hero in heroes]


@app.route('/heroes/<int:id>')
def hero_by_id(id):
    """Return a hero by id."""

    hero = Hero.query.get(id)

    if not hero:
        return {'error': 'Hero not found'}, 404

    return hero.to_dict()


@app.route('/powers')
def powers():
    """Get a list of all the powers."""

    powers = Power.query.all()
    return [power.to_dict(rules=('-hero_power_list', )) for power in powers]


@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def get_or_update_power(id):
    """Get a power by id or update a power by id."""

    power = Power.query.get(id)

    if request.method == 'GET':
        if not power:
            return {'error': 'Power not found'}, 404

        return power.to_dict(rules=('-hero_power_list', ))

    elif request.method == 'PATCH':
        try:
            for key, value in request.json.items():
                setattr(power, key, value)
            db.session.commit()
        except Exception as e:
            return {'error': str(e)}, 400

        return power.to_dict(rules=('-hero_power_list', ))


@app.route('/hero_powers', methods=['POST'])
def hero_powers():
    """Create a new hero power."""

    data = request.json
    try:
        new_hero_power = HeroPower(strength=data.get('strength'),
                                   power_id=data.get('power_id'),
                                   hero_id=data.get('hero_id'))
        db.session.add(new_hero_power)
        db.session.commit()

        return new_hero_power.to_dict(), 201
    except Exception as e:
        return {'errors': str(e)}


if __name__ == '__main__':
    app.run(port=5555, debug=True)
