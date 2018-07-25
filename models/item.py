# The RESOURCE normally has to use the MODEL to extract data from the DB. The MODEL kinda stands on itself.
# Aca van los methods that are not called by an API directly (que son los
# get/post/put/del). They are only used from within our code. So we don't put
# these methods in the resource package
import sqlite3
from db import db

# ItemModel is our INTERNAL representation so it has to contain the properties of an item as object properties.
# This is going to tell the SQLAlchemy entity that this ItemModel class will be saved to a database and
# retrieved from a DB. It's going to create that mapping between the DB and this object.
class ItemModel(db.Model):
    __tablename__ = 'items'                          # We told our app that we have two models (User and Item) that
    id = db.Column(db.Integer, primary_key=True)     # are coming from tables from our DB. And we've told SQLAlchemy
    name = db.Column(db.String(80))                  # how it can read this items: by just looking at the columns and
    price = db.Column(db.Float(precision=2))         # it will plug it in straight to the init method and create an object for each rown in our DB. The id property will also be passed in but it won't be used because there's no id on the init method.
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))  # a foreign key references the ID of Stores
    store = db.relationship('StoreModel')            # automaticamente hace el join items-->store (so we avoid using SQL joins in SQLAlchemy).
    # So now every ItemModel has a property 'store' that's the store which matches this store_id

    def __init__(self, name, price, store_id):    # each item has a store_id associated
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):     # returns a JSON representation of the item(a dictionary)
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # which is the same as "SELECT * FROM items WHERE name=name LIMIT 1" and returns an ItemModel object

    def save_to_db(self):                               # self is an object item
        db.session.add(self)                        # the session in this instance is a collection of objects that we'll write to the DB
        db.session.commit()                         # We can add multiple objects to the session and then write them all at once (more efficient)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
