from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'heroes_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    serialize_rules = '-hero.hero_powers', '-power.hero_power_list'

    @validates('strength')
    def validate_strength(self, key, value):
        """
        Validate that the strength for a HeroPower is one of 'Strong', 'Weak', 'Average'.
        Otherwise, raise a ValueError.
        """
        valid_values = ['Strong', 'Weak', 'Average']
        if not value in valid_values:
            raise ValueError(f'Hero {key} must be one of {valid_values}')
        return value


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String, unique=True)

    hero_powers = db.relationship('HeroPower',
                                  backref='hero',
                                  cascade='all, delete-orphan')
    powers = association_proxy('hero_powers', 'power')

    serialize_rules = '-hero_powers.hero',


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)

    hero_power_list = db.relationship('HeroPower',
                                      backref='power',
                                      cascade='all, delete-orphan')
    heroes = association_proxy('hero_power_list', 'hero')

    serialize_rules = '-hero_power_list.power',

    @validates('description')
    def validate_description(self, key, value):
        """
        Validate that the description for a Power is at least 20 characters long.
        Otherwise, raise a ValueError.
        """
        if not (value and len(value) > 20):
            raise ValueError(f'Hero {key} must be at least 20 characters long')
        return value
