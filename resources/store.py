from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):    # what endpoints do we need for a store resource? getp, post and delete endpoints, but not put (no store editing)
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()              # devuelve el codigo 200 x default. No hace falta declararlo
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):    # si existe dicho store..
            return {'message', "A store with name '{}' already exists.".format(name)}, 400
        store = StoreModel(name)   # a crear el nuevo store
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store.'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}  # return a dictionary with a list of stores
