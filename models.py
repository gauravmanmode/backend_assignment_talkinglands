from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry

db = SQLAlchemy()

class MultiPointModel(db.Model):
    __tablename__ = "multipoints"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    location = db.Column(Geometry("MULTIPOINT", srid=4326))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class MultiPolygonModel(db.Model):
    __tablename__ = "multipolygons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    shape = db.Column(Geometry("MULTIPOLYGON", srid=4326))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
