from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_character= db.relationship("FavoriteCharacter", back_populates="user")
    favotire_planet=db.relationship("FavoritePlanet", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Planet(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    population = db.Column(db.Integer, nullable=True)  
    favorite_planet=db.relationship("FavoritePlanet", back_populates="planet")

class Character(db.Model):
    id=db.Colum(db.Integer,primary_key=True)  
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(20), nullable=True)
    height = db.Column(db.Integer, nullable=True)
    mass = db.Column(db.Integer, nullable=True)  
    favorite_character=db.relationship("FavoriteCharacter",back_populates="character")

class FavoriteCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    user=db.relationship("User",back_populates="favorite_character")
    character=db.relationship("Character", back_populates="favorite_character")

class FavoritePlanet(db.Model):
    id=db.Column(db.Interger,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    planet_id=db.Column(db.Integer,db.ForeignKey('planet.id'),nullable=False)
    user=db.relationship("User",back_populates="favorite_planet")
    planet=db.relationship("Planet",back_populates="favorite_planet")