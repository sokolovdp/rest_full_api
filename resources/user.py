from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from models.user_model import UserModel
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import exc


class UserRegister(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument('username',
                             type=str,
                             required=True,
                             help="username must be present")
    user_parser.add_argument('password',
                             type=str,
                             required=True,
                             help="password must be present")

    @classmethod
    def post(cls):
        user_data = cls.user_parser.parse_args()
        user_name = user_data['username']
        password_hashed = generate_password_hash(user_data['password'], salt_length=16)
        user = UserModel.find_by_username(user_name)
        if user:
            return {'message': "error - duplicated username"}, 400
        else:
            user = UserModel(user_name, password_hashed)
            try:
                user.save_to_database()
            except sqlalchemy.exc.DatabaseError:
                return {'message': "internal database error"}, 500
            else:
                return {'message': "user created"}, 201
