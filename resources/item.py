# The RESOURCE normally has to use the MODEL to extract data from the DB. The MODEL kinda stands on itself.
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel            # del archivo models/itemp.py, agregar la class ItemModel

# The API works with Resources and every resource has to be a class:
class Item(Resource):   # for example, the class Item that then inherits from the class Resource.
    parser = reqparse.RequestParser()     # initializes a new object which we can use to the request
    parser.add_argument('price',          # this is going to look in the JSON payload (but also it will look in html FORM payloads)
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',          # this is going to look in the JSON payload (but also it will look in html FORM payloads)
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()          # this means that we have to authenticate before we can call the get method
    def get(self,name):                            # retrieve an item from the DB
        item = ItemModel.find_by_name(name)        # item is an object
        if item:
            return item.json()                     # we need to return a JSON format of the item, so we convert it from object to JSON representation
        return {'message': 'Item not found'}, 404

    def post(self, name):                              # POST crea un item, pero NO actualiza un item
        if ItemModel.find_by_name(name):                    # it can also be called Item.find_by_name(name)
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()          # this is going to parse the arguments that come through the JSON paylod and it's gonna put the valid ones in data
        item = ItemModel(name, **data)        # Whenever we create an item model, we need to pass in the store_id. **data --> data['price'], data['store_id']
        try:
            item.save_to_db()                  # the item object of the ItemModel class has an 'insert' method defined on the models/item.py file
        except:
            return {'message': "An error occurred inserting the item." }, 500  # devuelvo 500 xq es un server error
        return item.json(), 201  # I tell postman or mobile app that it was appended successfully (201 created // 202 accepted). Always return Json format!

    def delete(self, name):    # aca no va el request.json() porque al item name lo estoy mandando en el endpoint /item/piano x ej
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):                        # PUT method can both insert an item or update an item
        data = Item.parser.parse_args()          # this is going to parse the arguments that come through the JSON paylod and it's gonna put the valid ones in data
        item = ItemModel.find_by_name(name)           # item is an ItemModel object found in the database. Encuentra el item en la DB  o no lo encuentra.

        if item is None:                                  # if we didn't find an item in the database
            item = ItemModel(name, **data)        # Whenever we create an item model, we need to pass in the store_id. ** data --> data['price'], data['store_id']
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()             # devuelve el JSON format de la updated_item object (que es un ItemModel class)

# PUT is an idempotent action --> you can call the same request many times in a row and the output should never change.
# Therefore PUT can be used to both create items or update an existing item

class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
