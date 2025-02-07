from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ ="user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(),  nullable=False)
    favorite= db.relationship("Favorite", back_populates="user")
    

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Planet(db.Model):
    __tablename__ ="planet"
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    population = db.Column(db.Integer, nullable=True)  
    favorite=db.relationship("Favorite", back_populates='planet',lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }

class Character(db.Model):
    __tablename__ ="character"
    id=db.Column(db.Integer,primary_key=True)  
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(20), nullable=True)
    height = db.Column(db.Integer, nullable=True)
    mass = db.Column(db.Integer, nullable=True)  
    favorite=db.relationship("Favorite",back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
        }

class Favorite(db.Model):
    __tablename__ ="favorite"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    user = db.relationship("User", back_populates="favorite")
    planet = db.relationship("Planet", back_populates="favorite")
    character = db.relationship("Character", back_populates="favorite")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "character": self.character.serialize() if self.character else None,
            "planet": self.planet.serialize() if self.planet else None,
        }

