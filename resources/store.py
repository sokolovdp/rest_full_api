from flask_restful import Resource, reqparse  # return data in JSON format
from flask_jwt import jwt_required
from models.store_model import StoreModel
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import exc


# from flask_jwt import JWTError
# @app.errorhandler(JWTError)
# def on_auth_error():
#     return jsonify({'message': 'There was an error with your JWT token!'}), 401

class Store(Resource):
    method_decorators = [jwt_required()]

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Store must have a name")

    @jwt_required()
    def get(self, store_name):
        store = StoreModel.find_by_name(store_name)
        if store:
            return store.json(), 200
        else:
            return {"store": None}, 404

    @jwt_required()
    def post(self, store_name):
        if StoreModel.find_by_name(store_name):
            return {"message": "error - duplicated name"}, 400  # bad request

        store = StoreModel(store_name)
        try:
            store.save_to_database()
        except sqlalchemy.exc.DatabaseError:
            return {"message": "error - internal database error"}, 500
        else:
            return {"name": store.name, "store_id": store.id}, 201  # created

    @jwt_required()
    def delete(self, store_name):
        store = StoreModel.find_by_name(store_name)
        if store:
            try:
                store.delete_from_database()
            except sqlalchemy.exc.DatabaseError:
                return {"message": "error - internal database error"}, 500
        return {"store": "deleted"}, 200


class StoreList(Resource):
    method_decorators = [jwt_required()]

    @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.get_all_stores()]}
