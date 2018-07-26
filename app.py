import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity       # import methods from .py files
from resources.user import UserRegister           # import methods from resources/user.py (now 'resources' is a package because it contains" __init__.py")
from resources.item import Item, ItemList         # import methods from resources/item.py (now 'resources' is a package because it contains" __init__.py")
from resources.store import Store, StoreList

# Flask is gona be our app, and our app is gonna have all these routes, and then
# we can create new routes and assign methods to them.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')  # get the environmrnt variable, otherwise sql lite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # don't turn off the flask SQLAlchemy modification tracker
app.secret_key = 'jose'
api = Api(app)   # api will allow us to very easily add these Resources (get, post, etc) to it

jwt = JWT(app, authenticate, identity) # when we initialize the JWT object, our app will use the authenticate and identity to allow for authentication of users.
# JWT create a new endpoint /auth. When we call /auth, we send it a username and password. And the JWT extension gets that username and password and
# sends it over to the authenticate function that takes in a username and password and compares the passwords, and returns a User object
# The auth endpoint returns a JWT token which we use for the next request we make (a get or post for example). So when we send the JWT Token, JWT calls
# the identity function (payload) which uses the JWT token to get the user_id

api.add_resource(Item, '/item/<string:name>')
# this tells the API: the resource Item now is gonna be accessible via our API through the enpoint '/item/<string:name>'.
# And 'name' will be a parameter to the get/post/put method of the Item class/Resource
api.add_resource(ItemList, '/items')           # http://127.0.0.1:5000/items
api.add_resource(UserRegister, '/register')   # When we execute a POST request to the endpoint /register, it's gonna call UserRegister which will call the POST method
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':                   # Esto sirve para que corra la app si ejecutamos "python app2.py". Eso ocurre xq __main__ es app2.py en este caso.
    from db import db                        # to prevent circular imports
    db.init_app(app)                         # initialize db with our flask app
    app.run(port=5000, debug=True)           # Pero si hacemos "import app2.py", no la ejecuta porque no es __main__
