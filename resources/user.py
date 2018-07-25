import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
# A Resource is just a thing that our API can return and create and things like that.
# A resource is things that the API responds with, things that API clients can ask for.
# A resource is what the API thinks of. The API deals with resources such as users,
# items, stores, students. Similar to Object Oriented Programming
# A resource is used to map endpoints such as the GET or POST verb to the /item/name.
# A resource is only containing methods that the API interact with because it makes
# things easier in the long-ter for us to modify the code.
# Resources are usually mapped into DB tables as well.

# UserRegister is gonna be a Resource so we can add it to the API using flask_restful.
# We could just create a flask endpoint to register users but it's the same.
# But the good thing about using flask_restful and matking this UserRegister
# a Resource is that we only need to do a POST method.
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',    # en el body POST, tiene que estar el 'username' en json format
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument('password',    # en el body POST, tiene que estar el 'password' en json format
        type=str,
        required=True,
        help="This field cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()   # parse the arguments using the UserRegister parser
        if UserModel.find_by_username(data['username']):     # verifica que no exista el usuario ya
            return {'message': "A user with that username already exists"}, 400
        user = UserModel(**data)    # **data can be unpacked as data['username'], data['password']
        user.save_to_db()
        return {"message": "User created successfully."}, 201
