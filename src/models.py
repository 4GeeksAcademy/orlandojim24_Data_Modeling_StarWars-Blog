from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from eralchemy2 import render_er

# Initialize SQLAlchemy instance
db = SQLAlchemy()

Base = db.Model

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }

class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(20))
    eye_color: Mapped[Optional[str]] = mapped_column(String(50))
    birth_year: Mapped[Optional[str]] = mapped_column(String(20))

    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[Optional[str]] = mapped_column(String(120))
    terrain: Mapped[Optional[str]] = mapped_column(String(120))

    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey('character.id'), nullable=True)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey('planet.id'), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    character: Mapped[Optional["Character"]] = relationship("Character", back_populates="favorites")
    planet: Mapped[Optional["Planet"]] = relationship("Planet", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
        }

# Generate the diagram
render_er(Base, 'diagram.png')
