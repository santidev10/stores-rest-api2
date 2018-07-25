# Our class User is not a resource because the API cannot receive data into
# this class or send this class as a JSON representation. This class User
# is a helper essentially that we use to store some data about the user
# and also a helper that contains a couple of methods that allow us to easily
# retrieve User objects from a database. That's what a MODEL is:
# A MODEL is our INTERNAL representation of an entity whereas a RESOURCE is the
# EXTERNAL representation of an entity. Our API clients, like a website or a
# mobile app,think they are interacting with resources, that's what they see.
# And when our API responds, it responds with resources.
import sqlite3
from db import db

# UserModel is our INTERNAL representation so it has to contain the properties of an item as object properties.
# This is going to tell the SQLAlchemy entity that this UserModel class will be saved to a database and
# retrieved from a DB. It's going to create that mapping between the DB and this object.

class UserModel(db.Model):   # This USerModel is an API, not a Rest API with two interfaces or enpoints: find_by_username and find_by_id
    __tablename__ = 'users'                       # table name where UserModel is gonna be stored
    id = db.Column(db.Integer, primary_key=True)  # it also creates an index on id. It's the primary key --> autoincrementiung
    username = db.Column(db.String(80))           # limit the size of the username
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)                 #if you wanna remove from the DB, you'd put 'remove' instead of 'add'
        db.session.commit()

    @classmethod                                     # mapping by username
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod                                    # mapping by userid
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()                                    # return User object or None
