from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    super_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Define the relationship with HeroPower
    powers = db.relationship('HeroPower', backref='hero', lazy=True)

    def __init__(self, name, super_name, created_at, updated_at):
        self.name = name
        self.super_name = super_name
        self.created_at = created_at
        self.updated_at = updated_at

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Define the relationship with HeroPower
    heroes = db.relationship('HeroPower', backref='power', lazy=True)

    def __init__(self, name, description, created_at, updated_at):
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    __table_args__ = (
        CheckConstraint('length(description) >= 20', name='check_description_length'),
    )

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(255), CheckConstraint("strength IN ('Strong', 'Weak', 'Average')"))
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, strength, hero_id, power_id, created_at, updated_at):
        self.strength = strength
        self.hero_id = hero_id
        self.power_id = power_id
        self.created_at = created_at
        self.updated_at = updated_at
