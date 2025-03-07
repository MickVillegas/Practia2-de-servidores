from sqlalchemy import Boolean, Column, ForeignKey, DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class Categorias(db.Model):
    """Categorías de los artículos"""
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    articulos = relationship("Articulos", backref="Categorias", lazy='dynamic')
class Articulos(db.Model):
    """Artículos de nuestra tienda"""
    __tablename__ = 'articulos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, default=0)
    iva = Column(Integer, default=21)
    descripcion = Column(String(255))
    image = Column(String(255))
    stock = Column(Integer, default=0)
    CategoriaId = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    categoria = relationship("Categorias", backref="Articulos")
    def precio_final(self):
        return self.precio + (self.precio*self.iva/100)
class Usuarios(db.Model):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key = True)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    admin = Column(Boolean, default=False)
@property
def password(self):
    raise AttributeError("Estas haciendo algo ilegalisimo")

@password.setter
def password(self, password):
    self.password_hash = generate_password_hash(password)
def verify_password(self, password):
    return check_password_hash(self.password_hash, password)