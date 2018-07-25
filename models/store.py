from db import db

class StoreModel(db.Model):     # create the StoreModel and link it up with the item
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy='dynamic')   # Backreference: it allows a store to see which items (in the items table) with store_id equal to its own id
# so SQLAlchemy is saying "StoreModel has a relationship with ItemModel. Automaticamente hace el join [1 store--> muchos items]. Por lo tanto,
# the property 'items' is a list of ItemModels. As soon as a StoreModel is created, the relationship is created as well, we're gonna create
# an object for each item in the DB that matches that store_id. But that can be expensive. We can tell SQLAlchemy to not do that relationship in advace:
# to not go into the items table and create and object for each item YET (lazy dynamic). And now, whenever we access the json method, we're gonna
# get an error unless we use .ALL(). When we use 'lazy=dynamic', 'self.items' no longer is a list of items. Now it's a query builder that has
# the ability to look into the items table. Then we can use ".all()" to retrieve all the items in that table. Which means that until we call the
# json() method, we are not looking into the table, which means that creating stores is very simple. However, it also means that every time we
# call the json() method, we have to go into the table. So then it's gonna be slower if we use 'lazy=dynamic' because the relationship is not created
# in advance. So there's a trade-off between speed of creation of the StoreModel and speed of calling the json() method.
    pass

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}   # 'items' is a list of items

    @classmethod
    def find_by_name(cls, name):                 # retrieve a store by its name
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):                         # save a store ro the DB
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):                    # delete a store from the DB
        db.session.delete(self)
        db.session.commit()
