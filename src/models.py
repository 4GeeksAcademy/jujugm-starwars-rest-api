from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, ForeignKey

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(80))
    is_active: Mapped[bool]

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String(80), nullable=False) 
    hair_color: Mapped[str]= mapped_column(String(80), nullable=True) 
    skin_color: Mapped[str] = mapped_column(String(80),nullable=False) 
    gender: Mapped[str] = mapped_column (String(80),nullable=False) #todos deben tener nullable false si no no se hacen

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
           
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planet'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String(80), nullable=False) 
    population: Mapped[str]= mapped_column(String(80), nullable=False) 
    terrain: Mapped[str] = mapped_column(String(80), nullable=False) 
    climate: Mapped[str] = mapped_column (String(80), nullable=False) #todos deben tener nullable false si no no se hacen



    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate

            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(Integer, ForeignKey('people.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(Integer, ForeignKey('planet.id'), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id
        }




    # from flask_sqlalchemy import SQLAlchemy

    # db = SQLAlchemy()

    # class User(db.Model):
    #  id = db.Column(db.Integer, primary_key=True)
    #  email = db.Column(db.String(120), unique=True, nullable=False)
    #  password = db.Column(db.String(80), unique=False, nullable=False)
    #  is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    #  def __repr__(self):
    #      return '<User %r>' % self.username

    #  def serialize(self):
    #      return {
    #          "id": self.id,
    #          "email": self.email,
    #         # do not serialize the password, its a security breach
    #      }