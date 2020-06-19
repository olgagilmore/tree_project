import os
from sqlalchemy import Column, String, Integer, Enum, Float, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.sql.sqltypes import DateTime
from click.types import STRING
import enum

from flask_migrate import Migrate

# database_name = "trees4life"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = os.environ['DATABASE_URL']
print(database_path)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

# '''
# tree_owner
# '''
# tree_owner = db.Table('tree_owner',
#     db.Column('owner_id', db.Integer, db.ForeignKey('Owner.id'),
#                primary_key=True),
#     db.Column('tree_id', db.Integer, db.ForeignKey('Tree.id'),
#                primary_key=True)
# )


class Owner(db.Model):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    first_name = Column(db.String(), nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)

    # trees = db.relationship('Tree', secondary=tree_owner,
    trees = db.relationship('Tree',
                            backref=db.backref('owner', lazy=True))

    def __init__(self, firstNm, lastNm, email, phone, addr):
        self.first_name = firstNm
        self.last_name = lastNm
        self.email = email
        self.phone = phone
        self.address = addr

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'first_name':  self.first_name,
          'last_name': self.last_name,
          'mail': self.email,
          'phone': self.phone,
          'address': self.address
        }
    # check on secondary association


class TreeTypeEnum(enum.Enum):
    live_oak = 1
    mahogany = 2
    bald_cypress = 3
    maple = 4
    elm = 5
    other = 6


class Tree(db.Model):
    __tablename__ = 'trees'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(TreeTypeEnum), nullable=False)
    # description = Column(String)
    owner_id = Column(Integer, db.ForeignKey('owners.id'), nullable=False)
    # GPS coordinates
    latitude = Column(Float)
    longitude = Column(Float)

    # receivedDate = Column(DateTime, nullable=False)
    plantedDate = Column(Date)
    # status = Column(String)
    # picture = Column(db.LargeBinary)

    def __init__(self, type, own_id, lat, long, datePlanted):
        self.type = type
        self.owner_id = own_id
        self.latitude = lat
        self.longitude = long
        self.plantedDate = datePlanted

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'owner_id': self.owner_id,
          'type': self.type.name,
          'lat': self.latitude,
          'long': self.longitude,
          'planted_date': self.plantedDate
        }

# '''
# TreeType
# '''
# class TreeType(db.Model):
#   __tablename__ = 'categories'
#   id = Column(Integer, primary_key=True)
#   type = Column(String)
#   description =Column(String)
#   trees= db.relationship('Tree', 'tree_type', lazy=True)
#
#   def __init__(self, type, desc):
#     self.type = type
#     self.description=desc
#
#   def format(self):
#     return {
#       'id': self.id,
#       'type': self.type,
#       'description': self.description
#     }
#
